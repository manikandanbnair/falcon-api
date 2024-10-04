import falcon
from handler.exception_handler import ValidationException
from rest.UserRest import UserResource
from mongo_manager.connection import DatabaseConnection
from routes.routes import register_routes

app = falcon.App()

db_connection = DatabaseConnection().get_db()
user_resource = UserResource(db_connection)
register_routes(app,db_connection)

app.add_error_handler(ValidationException, ValidationException.validation_exception_handler)


