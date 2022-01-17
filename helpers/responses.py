class AppResponse:
    def __init__(self, message, is_error=False):
        self.message = message
        self.is_error = is_error

    def __str__(self):
        return self.message

    def unknown_error_body(self, code=101):
        return {
            'error': self.message,
            'code': code,
        }

    def success_body(self, code=200):
        return {
            'success': self.message,
            'code': code
        }
