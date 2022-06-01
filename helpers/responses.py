class AppResponse:
    def __init__(self, message, is_error=False):
        self.message = message
        self.is_error = is_error

    def __str__(self):
        return self.message

    def body(self):
        return {
            'success': self.message,
            'code': 200
        }

    def error_body(self):
        return {
            'error': self.message
        }
