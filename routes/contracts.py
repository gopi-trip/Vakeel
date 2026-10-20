from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from app.config import ALLOWED_EXTENSIONS
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