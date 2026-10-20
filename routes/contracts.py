from fastapi import APIRouter, UploadFile, File
import os

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

