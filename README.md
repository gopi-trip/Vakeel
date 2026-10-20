# Vakeel

Vakeel is a FastAPI project for contract document intake and analysis. The current codebase provides the API skeleton, MongoDB initialization, and an in-progress PDF/TXT upload and text-extraction flow. Contract analysis and persistence are not yet implemented end to end.

## Current Features

- FastAPI application titled **Vakeel Contract API**.
- MongoDB connection configured through `MONGODB_URI`.
- Startup initialization creates the `contracts` and `analysis` collections and unique indexes on `contract_id` and `analysis_id`.
- A `POST /contracts/upload` endpoint is defined for PDF and TXT uploads.
- PDF text extraction uses PyPDF2; TXT files are read as UTF-8.

## Requirements

- Python and pip
- Docker with the Docker Compose plugin, or a MongoDB server reachable from the API

Install the Python dependencies from the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell, activate the virtual environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Configure MongoDB

Start the local MongoDB service from the repository root:

```bash
docker compose up -d mongodb
```

The Compose service publishes MongoDB on port `27017` and persists its data in the `mongodb_data` Docker volume. The current Compose file includes development credentials directly in the file; replace them or move them to a private environment file before sharing or deploying it. MongoDB's root user authenticates against the `admin` database.

Create `app/.env` and set `MONGODB_URI` to a URI matching the credentials configured for the MongoDB service:

```dotenv
MONGODB_URI=mongodb://<username>:<password>@localhost:27017/?authSource=admin
```

Replace `<username>` and `<password>` with the MongoDB credentials. If using a remote MongoDB instance, set `MONGODB_URI` to its connection string instead. Do not commit real credentials.

## Run the API

From the repository root, with the virtual environment activated and MongoDB running:

```bash
uvicorn main:app --app-dir app --reload
```

The `--app-dir app` option matches the current module imports. The interactive API documentation is available at `http://127.0.0.1:8000/docs`; ReDoc is at `http://127.0.0.1:8000/redoc`.

## API

### `POST /contracts/upload`

Accepts a multipart form upload with a field named `file`. The configured extensions are `.pdf` and `.txt`.

Example request:

```bash
curl -X POST http://127.0.0.1:8000/contracts/upload \
	-F "file=@./contract.pdf"
```

The current handler is unfinished and should not yet be treated as a reliable upload endpoint: its generated filename calls the UUID `hex` property as a function, its size calculation does not correctly convert bytes to megabytes, and it does not return the extracted text or save a contract record in MongoDB. The configured upload directory is `uploads/` relative to the API process working directory.

The root endpoint (`GET /`) lists planned contract and analysis routes. Only the upload route is currently registered; analysis endpoints and Gemini integration are not present in the current implementation.

## Project Layout

```text
app/
	config.py                 Environment and upload configuration
	database.py               MongoDB client, collections, and indexes
	main.py                   FastAPI app and router registration
	routes/contracts.py       Contract upload endpoint
	service/document_parser.py PDF and TXT text extraction
docker-compose.yml          Local MongoDB service
requirements.txt            Python dependencies
```

## Data and Development Notes

- The MongoDB database name is `mydb`, as configured in `app/database.py`.
- The configured collections are `contracts` and `analysis`.
- Uploaded files are stored on the local filesystem; the Compose volume only persists MongoDB data.
- The current API does not yet persist uploaded contract metadata or extracted text, or provide retrieval and analysis endpoints.
