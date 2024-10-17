import falcon, json
from handler.exception_handler import ValidationException
from service.UserService import UserModel, User
from routes.routes import route


@route("/users")
class UserResource:
    def __init__(self):
        self.user_model = UserModel()

    def on_get(self, req, resp):
        email = req.params.get("email")
        if not email:
            users = self.user_model.find_all()
            userMessage = "Users"
            users_data = json.loads(users)
        else:
            user = self.user_model.find_by_email(email)
            userMessage = "User"
            users_data = json.loads(user)
        resp_message = {userMessage: users_data}
        resp.status = falcon.HTTP_200
        resp.text = json.dumps(resp_message)


@route("/user")
class UserPost:
    def __init__(self):
        self.user_model = UserModel()

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

        self.user_model.user_validation(age, email)
        user = User(name, age, email)


        data = {"name": name, "age": age, "email": email}

        try:
            with open("user_data.json", "r+") as file:
                file.seek(0)

                old_data = json.load(file)
                if not isinstance(old_data, list):
                    old_data = [old_data]

                old_data.append(data)
                file.seek(0)
                file.truncate()
                json.dump(old_data, file)
        except Exception:
            raise ValidationException("Error in writing file.")

        self.user_model.create(user)

        resp_message = {"message": "Successfully created"}
        resp.status = falcon.HTTP_201
        resp.text = json.dumps(resp_message)


