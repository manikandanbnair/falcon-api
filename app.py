import falcon
from handler.exception_handler import ValidationException
from rest.UserRest import UserResource

from routes.routes import register_routes

app = falcon.App()

register_routes(app)

app.add_error_handler(ValidationException, ValidationException.validation_exception_handler)
