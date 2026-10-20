from email.policy import HTTP
from genericpath import exists
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException
import os

from opentelemetry.propagate import extract
from config import ALLOWED_EXTENSIONS,MAX_ALLOWED_FILE_SIZE_MB, UPLOAD_DIR
from service.document_parser import extract_text

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

    file_size = len(content)/1024*1024

    if file_size > MAX_ALLOWED_FILE_SIZE_MB:
        raise HTTPException(
            status_code=413,
            detail="File size too large"
        )

    # Save the file to a local directory
    
    os.makedirs(UPLOAD_DIR, exist_ok=True) # Make the directory if one doesn't exist
    file_name = f"{uuid.uuid4().hex()}{ext}" # Give the file a unique name followed by its extension

    file_path = os.path.join(UPLOAD_DIR,file_name) # Get a file path of the form UPLOAD_DIR + file_name

    with open(file_path,"wb") as f:
        f.write(content) # Write the read contents to the created file. 

    parsed = extract_text(file_path)