import logging

from pymongo import MongoClient, errors


class DbConfig:
    def __init__(self, db_name, connection_string):
        self.db_name = db_name
        self.connection_string = connection_string
        self.client = None
        self.database = None
        self.connect()

    def connect(self):
        try:
            self.client = MongoClient(self.connection_string)
            self.database = self.client[self.db_name]
            logging.info(f"Connected to MongodbB database: {self.db_name}")
        except errors.ConfigurationError as e:
            raise Exception(f"Failed to connect to MongoDB: {str(e)}")

    def insert_data(self, collection_name, new_data):
        try:
            if not isinstance(new_data, dict):
                raise ValueError("Data to insert must be a dictionary.")

            collection = self.database[collection_name]
            result = collection.insert_one(new_data)
            logging.info(f"Data inserted with ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            logging.error(f"Error inserting data into MongoDB: {str(e)}")
            raise

    def close_connection(self):
        if self.client:
            self.client.close()
            logging.info("MongoDB connection closed.")
