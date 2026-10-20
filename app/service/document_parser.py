import os

def extract_text_from_txt(filepath: str) -> str:

    with open(filepath,"r", encoding="utf-8") as f:
        return f.read()

def extact_text(file_path:str) -> str:
    # Extract the file extension
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError("Unsupported File format")