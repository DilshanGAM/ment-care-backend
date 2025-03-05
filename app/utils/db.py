from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Database:
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI")
        db_name = os.getenv("MONGO_DB_NAME")
        
        if not mongo_uri or not db_name:
            raise ValueError("MONGO_URI and MONGO_DB_NAME must be set in .env")

        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]

# Create a single instance of the database connection
db = Database()
