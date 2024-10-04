import falcon, json
from handler.exception_handler import ValidationException
from service.UserService import UserModel, User
from routes.routes import route

@route("/users")
@route("/users/email")
class UserResource:
    def __init__(self,db):
        self.user_model = UserModel(db)

    def on_get(self, req, resp):
        email = req.params.get("email")
        if not email:
            users = self.user_model.find_all()
            userMessage = "Users"
            users_data = json.loads(users)
            if not users_data:
                users_data = "No users present"
        else:
            user = self.user_model.find_by_email(email)
            userMessage = "User"
            users_data = json.loads(user)
            if not users_data:
                users_data = "User not found"

        resp_message = {userMessage: users_data}
        resp.status = falcon.HTTP_200
        resp.text = json.dumps(resp_message)

    def on_post(self, req, resp):
        data = json.loads(req.bounded_stream.read().decode('utf-8'))
        required_fields = ["name", "age", "email"]

        if not all(field in data for field in required_fields):
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"message": "Missing required fields. Please check your data and try again."})
            return



        name = data.get("name")
        age = data.get("age")
        email = data.get("email")

        self.user_model.user_validation(name, age, email)
        user = User(name, age, email)
        self.user_model.create(user)

        data = {"name": name, "age": age, "email": email}

        try:
            with open("user_data.json", "r+") as file:
                file.seek(0)
                try:
                    old_data = json.load(file)
                    if not isinstance(old_data, list):
                        old_data = [old_data]
                except json.JSONDecodeError:
                    old_data = []
                old_data.append(data)
                file.seek(0)
                file.truncate()
                json.dump(old_data, file)
        except Exception:
            raise ValidationException("Error in writing file.")

        resp_message = {"message": "Successfully created"}
        resp.status = falcon.HTTP_201
        resp.text = json.dumps(resp_message)

