from rest_framework.views import exception_handler
# import library for Response
from rest_framework.response import Response

def app_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['code'] = response.status_code
    
    if response is None: 
        response = Response({'code': 500, 'error': exc.__str__()})

    return response