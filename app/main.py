from fastapi import FastAPI

app = FastAPI(
    title="Vakeel Contract API",
    description="AI Powered Contract Analysis using Gemini",
    version="0.1.0"
)

@app.get("/")
async def  root():
    return {
        "app":"Vakeel Contract API",
        "Version": "0.1.0",
        "endpoints":{
            "POST /contracts/upload ":"An endpoint for uploading a PDF or TXT file for analysis",
            "GET /contracts/": "Get all the contracts",
            "GET /contracts/{id}": "Get a contract based on its ID",
            "GET /analysis/analyze/{id}": "Analyze a contract using AI and return the result",
            "GET /analysis/{id}" : "Retrieve analysis based on its ID",
            "GET /analysis/{contract_id}": "Retrieve a list of analysis for a specified contract id"
        }
    }