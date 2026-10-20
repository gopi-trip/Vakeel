import os
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path:str) -> dict:
    # Make a PDF Reader
    reader = PdfReader(file_path)
    text = ""

    #Extract the text
    for page in reader.pages:
        text+=page.extract_text() + "\n"

    return {"text":text.strip(), "page_count": str(len(reader.pages)), "word_count":str(len(text.split()))}


def extract_text_from_txt(filepath: str) -> str:

    with open(filepath,"r", encoding="utf-8") as f:
        text = f.read()
    return {
        "text":text.strip(),
        "page_count": "1",
        "word_count":str(len(text.split()))
    }

def extract_text(file_path:str) -> str:
    # Extract the file extension
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError("Unsupported File format")