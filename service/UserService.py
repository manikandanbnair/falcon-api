from dataclasses import dataclass
from bson import json_util
from handler.exception_handler import ValidationException, NotFoundException
from mongo_manager.mongo_manager import MongoManager


@dataclass
class User:
    name: str = None
    age: int = None
    email: str = None


class UserModel:

    _collection_name = "users"
    @classmethod
    def create(cls, user:User):
        user_data = user.__dict__
        MongoManager.insert(user_data,cls._collection_name)

    @classmethod
    def find_all(cls):
        users = MongoManager.find_all(cls._collection_name)
        data = list(users)
        if not data:
            raise NotFoundException("No users present")

        for user in data:
            user.pop('_id', None)
        return json_util.dumps(data)

    @classmethod
    def find_by_email(cls, email):
        user = MongoManager.find_by_email(email,cls._collection_name)
        if not user:
            raise NotFoundException("User not found")
        user.pop('_id',None)
        return json_util.dumps(user)

    @classmethod
    def exists_by_email(cls, email):
        user = MongoManager.find_by_email(email,cls._collection_name)
        if user:
            return True
        return False

    @classmethod
    def user_validation(cls,age,email):
        if not isinstance(age,int) or age < 0:
            raise ValidationException("Invalid age")
        if cls.exists_by_email(email):
            raise ValidationException("User already exists")


