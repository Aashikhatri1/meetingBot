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

cable_name_to_image_location = {
    'Line 1 (Virtual Audio Cable)': 'cables\\line_1.png',
    'Line 2 (Virtual Audio Cable)': 'cables\\line_2.png',
    'Line 3 (Virtual Audio Cable)': 'cables\\line_3.png',
    'Line 4 (Virtual Audio Cable)': 'cables\\line_4.png',
    'Line 5 (Virtual Audio Cable)': 'cables\\line_5.png',
    'Line 6 (Virtual Audio Cable)': 'cables\\line_6.png',    
    'Line 7 (Virtual Audio Cable)': 'cables\\line_7.png',
    'Line 8 (Virtual Audio Cable)': 'cables\\line_8.png',
    'Line 9 (Virtual Audio Cable)': 'cables\\line_9.png',
    'Line 10 (Virtual Audio Cable)': 'cables\\line_10.png',
    'Line 11 (Virtual Audio Cable)': 'cables\\line_11.png',
    'Line 12 (Virtual Audio Cable)': 'cables\\line_12.png',
    'Line 13 (Virtual Audio Cable)': 'cables\\line_13.png',
    'Line 14 (Virtual Audio Cable)': 'cables\\line_14.png',
    'Line 15 (Virtual Audio Cable)': 'cables\\line_15.png',
    'Line 16 (Virtual Audio Cable)': 'cables\\line_16.png',
    'Line 17 (Virtual Audio Cable)': 'cables\\line_17.png',
    'Line 18 (Virtual Audio Cable)': 'cables\\line_18.png',
    'Line 19 (Virtual Audio Cable)': 'cables\\line_19.png',
    'Line 20 (Virtual Audio Cable)': 'cables\\line_20.png',
    'Line 21 (Virtual Audio Cable)': 'cables\\line_21.png',
    'Line 22 (Virtual Audio Cable)': 'cables\\line_22.png',
    'Line 23 (Virtual Audio Cable)': 'cables\\line_23.png',
    'Line 24 (Virtual Audio Cable)': 'cables\\line_24.png',
    'Line 25 (Virtual Audio Cable)': 'cables\\line_25.png',
    'Line 26 (Virtual Audio Cable)': 'cables\\line_26.png',
    'Line 27 (Virtual Audio Cable)': 'cables\\line_27.png',
    'Line 28 (Virtual Audio Cable)': 'cables\\line_28.png',
    'Line 29 (Virtual Audio Cable)': 'cables\\line_29.png',
    'Line 30 (Virtual Audio Cable)': 'cables\\line_30.png',
    'Line 31 (Virtual Audio Cable)': 'cables\\line_31.png',
    'Line 32 (Virtual Audio Cable)': 'cables\\line_32.png'
}


class ServerHandler:
    @staticmethod
    def get_available_cable():
        """Fetches an available cable from the MongoDB collection."""
        document = collection.find_one({"name": "Server 1"})
        if document and document.get("availableCables"):
            available_cable_name = document["availableCables"][0]
            cable_image_location = cable_name_to_image_location.get(available_cable_name)
            if cable_image_location:
                return cable_image_location
        return None
    
    @staticmethod
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
print(ServerHandler.get_available_cable())  # get an available cable
print(
    ServerHandler.make_cable_available("Line 18 (Virtual Audio Cable)")
)  # move a cable from 'busy' to 'available'
