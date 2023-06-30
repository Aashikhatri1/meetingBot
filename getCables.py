from pymongo import MongoClient

class ServerHandler:
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client['YourDatabaseName']
        self.collection = self.db['YourCollectionName']

    def get_first_available_cable(self):
        server_data = self.collection.find_one({"_id": 1})  # assuming server id is 1
        if server_data and "availableCables" in server_data and server_data['availableCables']:
            return server_data['availableCables'][0]
        else:
            return None  # No available cable

    def move_cable_from_busy_to_available(self, cable_name):
        server_data = self.collection.find_one({"_id": 1})  # assuming server id is 1
        if server_data and "busyCables" in server_data and cable_name in server_data['busyCables']:
            # Remove the cable from busyCables list
            self.collection.update_one({"_id": 1}, {"$pull": {"busyCables": cable_name}})
            # Add the cable to availableCables list
            self.collection.update_one({"_id": 1}, {"$push": {"availableCables": cable_name}})
            return True
        else:
            return False  # Cable not found in busyCables list
