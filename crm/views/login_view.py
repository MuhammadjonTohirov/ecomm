from crm.serializers import UserSerializer
from crm.utils.utils import generate_access_token, generate_refresh_token
from helpers.responses import AppResponse


from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import datetime


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING)
        }
    ),
    responses={
        '200': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
                'expires_in': openapi.Schema(type=openapi.TYPE_STRING),
                'user': openapi.Schema(type=openapi.TYPE_OBJECT)
            })
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    User = get_user_model()
    username = request.data.get('username')
    password = request.data.get('password')
    response = Response()
    if (username is None) or (password is None):
        raise exceptions.AuthenticationFailed(AppResponse(
            'Username and password required', True).error_body())

    user = User.objects.filter(username=username).first()
    if (user is None):
        raise exceptions.AuthenticationFailed(
            AppResponse('User not found', True).error_body())
    if (not user.check_password(password)):
        raise exceptions.AuthenticationFailed(
            AppResponse('Wrong password', True).error_body())

    serialized_user = UserSerializer(user).data

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
    response.data = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expires_in': datetime.datetime.utcnow() + datetime.timedelta(days=50),
        'user': serialized_user,
    }

    return Response(AppResponse(response.data).body())
