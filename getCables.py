from pymongo import MongoClient
import os
import certifi
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

DB_CONNECTION = os.environ.get("DB_URI")
ca = certifi.where()

# Set up MongoDB client
client = MongoClient(DB_CONNECTION, tlsCAFile=ca)
db = client["Meeting_automation"]  # replace with your database name
collection = db["serverCables"]  # replace with your collection name

class ServerHandler:
    def get_available_cable():
        """Fetches an available cable from the MongoDB collection."""
        document = collection.find_one({"name": "Server 1"})
        if document and document.get("availableCables"):
            return document["availableCables"][0]  # return first available cable
        return None
    
    
    def make_cable_available(cable_name):
        """Moves a cable from 'busy' to 'available' in the MongoDB collection."""
        result = collection.update_one(
            {"name": "Server 1"},
            {
                "$pull": {"busyCables": cable_name},  # remove from 'busyCables'
                "$push": {"availableCables": cable_name},  # add to 'availableCables'
            },
        )
        return result.modified_count > 0  # return whether a document was modified


# Test the functions
print(get_available_cable())  # get an available cable
print(
    make_cable_available("Line 18 (Virtual Audio Cable)")
)  # move a cable from 'busy' to 'available'
