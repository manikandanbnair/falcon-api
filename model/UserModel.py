from dataclasses import dataclass

from bson import json_util

from handler.exception_handler import ValidationException


@dataclass
class User:
    name: str = None
    age: int = None
    email: str = None


class UserModel:

    def __init__(self, db):
        self.collection = db['users']


    def create(self, user:User):
        try:
            user_data = user.__dict__
            self.collection.insert_one(user_data)
        except Exception:
            raise Exception("Error creating user")



    def find_all(self):
        users = self.collection.find({}, {'_id': 0})
        data = list(users)
        return json_util.dumps(data)


    def find_by_email(self, email):
        user = self.collection.find_one({'email': email},{'_id': 0})
        return json_util.dumps(user)

    def exists_by_email(self, email):
        return self.collection.find_one({'email' : email})

    def user_validation(self,name,age,email):
        if not isinstance(age,(int)) or age < 0:
            raise ValidationException("Invalid age")
        if self.exists_by_email(email):
            raise ValidationException("User already exists")


