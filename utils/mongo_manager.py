import os
import pymongo
from dotenv import load_dotenv
MongoClient = pymongo.MongoClient


class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.client = cls.connect_to_mongo()
        return cls._instance

    @staticmethod
    def connect_to_mongo():
        load_dotenv()
        mongo_host = os.getenv('MONGO_HOST')
        mongo_port = int(os.getenv('MONGO_PORT'))
        mongo_db_name = os.getenv('MONGO_DB_NAME')

        try:
            client = pymongo.MongoClient(
                host=mongo_host,
                port=mongo_port,
            )
            return client[mongo_db_name]
        except ConnectionError as e:
            raise Exception(f"Could not connect to MongoDB: {e}")


    def get_db(self):
        return self.client