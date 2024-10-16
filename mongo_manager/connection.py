import configparser
import pymongo

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
        config = configparser.ConfigParser()
        config.read('config.ini')

        mongo_host = config['database']['MONGO_HOST']
        mongo_port = int(config['database']['MONGO_PORT'])
        mongo_db_name = config['database']['MONGO_DB_NAME']

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
