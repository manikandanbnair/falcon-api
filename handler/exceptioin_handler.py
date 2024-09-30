import json,falcon


class ValidationException(Exception):
    pass

def validation_exception_handler(ex, req, resp, error):
    resp.status = falcon.HTTP_400
    resp.text = json.dumps({"message": str(ex)})