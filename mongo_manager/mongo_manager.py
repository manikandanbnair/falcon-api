from mongo_manager.connection import DatabaseConnection

class MongoManager:
    # def __init__(self, db_connection, collection_name):
    #     self.db_connection = db_connection
    #     self.collection = self.db_connection[collection_name]
    db_connection = DatabaseConnection().get_db()
    @classmethod
    def insert(cls, user_data,collection_name):
        try:
            collection = cls.db_connection[collection_name]
            collection.insert_one(user_data)
        except Exception:
            raise Exception("Error creating user")

    @classmethod
    def find_all(cls,collection_name):
        collection = cls.db_connection[collection_name]
        users = collection.find({})
        return users

    @classmethod
    def find_by_email(cls, email,collection_name):
        collection = cls.db_connection[collection_name]
        user = collection.find_one({'email': email})
        return user


