from pymongo import MongoClient

class MongoProducer:
    uri = "mongodb://mongo1"
    client = MongoClient(uri)
    database = client["minecraft_db"]
    collection = database["minecraft_collection"]


    def insert_to_mongo(self, logs):
        myDict = {"Log": logs}

        self.collection.insert_one(myDict)
        
        

