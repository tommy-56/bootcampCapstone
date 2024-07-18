import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pymongo import MongoClient
import json

class DataHandler(FileSystemEventHandler):
    def __init__(self, mongo_client, db_name, collection_name):
        self.mongo_client = mongo_client
        self.db_name = db_name
        self.collection_name = collection_name

    def on_created(self, event):
        if event.is_directory:
            return None

        else:
            file_path = event.src_path
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.update_db(data)
            os.remove(file_path)

    def update_db(self, data):
        db = self.mongo_client[self.db_name]
        collection = db[self.collection_name]
        collection.insert_one(data)
        print(f"Data from {data} inserted successfully")

if __name__ == "__main__":
    # MongoDB connection details
    mongo_host = os.getenv('MONGO_HOST', 'mongo')
    mongo_port = int(os.getenv('MONGO_PORT', 27017))
    mongo_db = os.getenv('MONGO_DB', 'test_db')
    mongo_collection = os.getenv('MONGO_COLLECTION', 'test_collection')

    # Connect to MongoDB
    client = MongoClient(mongo_host, mongo_port)

    # Set up the watchdog observer
    event_handler = DataHandler(client, mongo_db, mongo_collection)
    observer = Observer()
    data_directory = '/data'
    observer.schedule(event_handler, path=data_directory, recursive=False)

    # Start the observer
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()