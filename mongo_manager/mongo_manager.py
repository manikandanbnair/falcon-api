from mongo_manager.connection import DatabaseConnection

class MongoManager:
    def __init__(self, db_connection, collection_name):
        self.db_connection = db_connection
        self.collection = self.db_connection[collection_name]

    def insert(self, user_data):
        try:
            self.collection.insert_one(user_data)
        except Exception:
            raise Exception("Error creating user")

    def find_all(self):
        users = self.collection.find({}, {'_id': 0})
        return users

    def find_by_email(self, email):
        user = self.collection.find_one({'email': email}, {'_id': 0})
        return user

    def exists_by_email(self, email):
        return self.collection.find_one({'email': email})

