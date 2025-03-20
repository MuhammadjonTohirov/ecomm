class AppResponse:
    def __init__(self, message, is_error=False):
        self.message = message
        self.is_error = is_error

    def __str__(self):
        return self.message

    def body(self):
        return {
            'data': self.message,
            'code': 200 # ok
        }

    def error_body(self):
        return {
            'error': self.message,
            'code': 500 # internal server error
        }
    
    def access_denied(self):
        return {
            'error': self.message,
            'code': 403 # forbidden
        }
    
    def not_found(self):
        return {
            'error': self.message,
            'code': 404 # not found
        }

    def bad_request(self):
        return {
            'error': self.message,
            'code': 400 # bad request
        }
