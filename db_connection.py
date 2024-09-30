from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure, PyMongoError

class DatabaseConnection:
    def __init__(self):
        try:
            self.client = MongoClient('mongodb://localhost:27017/userdb')
            self.db = self.client['userdb']
        except (ConnectionFailure, OperationFailure, PyMongoError) as e:
            raise Exception("DB connection error" + e)

    def get_db(self):
        return self.db