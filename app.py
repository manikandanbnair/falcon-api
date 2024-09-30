import falcon
from resources.UserResource import UserResource

from handler.exception_handler import ValidationException


app = falcon.App()
app.add_route("/users", UserResource())
app.add_route("/users/{email}", UserResource())


app.add_error_handler(Exception, ValidationException.validation_exception_handler)

