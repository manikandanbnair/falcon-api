_error_handler = []

def register_exception(exception_class):
    def decorator(handler_function):
        _error_handler.append((exception_class, handler_function))
        return handler_function
    return decorator

def add_error_handler_function(app):
    for exception_class,handler_function in _error_handler:
        app.add_error_handler(exception_class,handler_function)