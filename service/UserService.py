from dataclasses import dataclass

from bson import json_util

from handler.exception_handler import ValidationException
from mongo_manager.connection import DatabaseConnection
from mongo_manager.mongo_manager import MongoManager


@dataclass
class User:
    name: str = None
    age: int = None
    email: str = None


class UserModel:

    def __init__(self):
        self.db_connection = DatabaseConnection().get_db()
        self.mongo_manager = MongoManager(self.db_connection,collection_name="users")

    def create(self, user:User):
        user_data = user.__dict__
        self.mongo_manager.insert(user_data)

    def find_all(self):
        users = self.mongo_manager.find_all()
        data = list(users)
        return json_util.dumps(data)


    def find_by_email(self, email):
        user = self.mongo_manager.find_by_email(email)
        return json_util.dumps(user)

    def exists_by_email(self, email):
        return self.mongo_manager.exists_by_email(email)

    def user_validation(self,name,age,email):
        if not isinstance(age,int) or age < 0:
            raise ValidationException("Invalid age")
        if self.exists_by_email(email):
            raise ValidationException("User already exists")


