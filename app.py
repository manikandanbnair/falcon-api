import falcon
from utils.add_error_handler import add_error_handler_function
from utils.auto_load import auto_load
from routes.routes import add_route

app = falcon.App()

auto_load() #load necessary modules
add_route(app) #dynamic route creation
add_error_handler_function(app) #dynamic error handler
