_routes = []
def route(path):
    def decorator(cls):
        _routes.append((path, cls))
        return cls
    return decorator

def add_route(app):
    for path, resource in _routes:
        app.add_route(path, resource())

