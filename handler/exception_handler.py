import falcon

class ValidationException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    @staticmethod
    def validation_exception_handler(ex, req, resp, params):
        resp.status = falcon.HTTP_400
        resp.media = {'message': ex.message}
class NotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    @staticmethod
    def notfound_exception_handler(ex, req, resp, params):
        resp.status = falcon.HTTP_404
        resp.media = {'message': ex.message}