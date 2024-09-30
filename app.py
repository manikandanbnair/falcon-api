import falcon
from resources.UserResource import UserResource

from handler.exceptioin_handler import validation_exception_handler

app = falcon.App()
app.add_route("/users", UserResource())
app.add_route("/users/{email}", UserResource())


app.add_error_handler(Exception, validation_exception_handler)
# app.add_error_handler(json.JSONDecodeError, json_decode_error_handler)
# app.add_error_handler(ValueError, value_error_handler)
