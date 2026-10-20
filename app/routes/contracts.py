from email.policy import HTTP
from genericpath import exists
from unittest import async_case
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException
import os

from opentelemetry.propagate import extract
from config import ALLOWED_EXTENSIONS,MAX_ALLOWED_FILE_SIZE_MB, UPLOAD_DIR
from service.document_parser import extract_text

from models import Contract
from database import contracts_collection

router = APIRouter(
    prefix="/contracts",
    tags=["Contracts"]
)

@router.post("/upload")
async def upload_contract(
    file: UploadFile = File(...) 
):
    """
    Upload a PDF or a TXT file here
    """
    ext = os.path.splitext(file.filename)[1].lower() # Get the extension of the file

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="File type not allowed"
        )

    content = await file.read()

    # Check the file size

    file_size = len(content)/(1024*1024)

    if file_size > MAX_ALLOWED_FILE_SIZE_MB:
        raise HTTPException(
            status_code=413,
            detail="File size too large"
        )

    # Save the file to a local directory
    
    os.makedirs(UPLOAD_DIR, exist_ok=True) # Make the directory if one doesn't exist

    file_name = f"{uuid.uuid4().hex}{ext}" # Give the file a unique name followed by its extension

    file_path = os.path.join(UPLOAD_DIR,file_name) # Get a file path of the form UPLOAD_DIR + file_name

    with open(file_path,"wb") as f:
        f.write(content) # Write the read contents to the created file. 

    parsed = extract_text(file_path)

    contract_data = Contract(
        file_name=file_name,
        original_name=file.filename,
        text_content=parsed["text"] if isinstance(parsed,dict) else parsed,
        page_count = int(parsed["page_count"]) if isinstance(parsed,dict) else len(parsed.splitlines()),
        word_count= int(parsed["word_count"]) if isinstance(parsed,dict) else len(parsed.split()),
    )

    doc = contract_data.model_dump() #Convert Pydantic Object into a dictionary
    result = contracts_collection.insert_one(doc)
    contract_data.id = str(result.inserted_id)

    return {
        "Message":"File Uploaded successfully",
        "contract" : contract_data.model_dump(),
        "contract_id": contract_data.id
    }

@router.get("/")
async def get_all_contracts():
    """
    List all the contracts
    """
    contracts = []
    for doc in contracts_collection.find({},{"text_content":0}):
        contract = Contract(**doc)
        contract.id = str(doc["_id"])
        contracts.append(contract.model_dump())

    return {
        "Contracts": contracts
    }

@router.get("/{contract_id}")
async def get_contract_by_id(contract_id:str):

    from bson import ObjectId
    
    doc = contracts_collection.find_one({"_id":ObjectId(contract_id)})

    if not doc:
        raise HTTPException(
            status_code=404,
            detail = f"A contract with the ID {contract_id} does not exist"
        )

    contract = Contract(**doc)
    contract.id = str(doc["_id"])

    return {
        "Contract":contract.model_dump()
    }
