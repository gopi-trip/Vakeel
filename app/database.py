from enum import unique

from pymongo import MongoClient
from app.config import MONGODB_URI

client = MongoClient(MONGODB_URI)
db = client.get_database()

#Create the collections
contracts_collection = db["contracts"]
analysis_collection = db["analysis"]

# Initialize the DB
def init_db():
    # Create the indexes for the collections if they don't exist
    contracts_collection.create_index("contract_id",unique=True)
    analysis_collection.create_index("analysis_id",unique=True)