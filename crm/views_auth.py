import datetime
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from crm.serializers import UserSerializer
from crm.utils import decode_token, generate_access_token, generate_refresh_token
from helpers.responses import AppResponse

@api_view(['POST'])
@permission_classes([AllowAny])
def new_token(request):
    refresh_token = request.data.get('refresh_token', None)
    if refresh_token is None:
        return Response(AppResponse('Refresh token is required').body())
    try: 
        refresh = decode_token(refresh_token, is_refresh_token=True)
        user_id = refresh['user_id']
        exp = refresh['exp']
        is_expired = exp < datetime.datetime.now().timestamp()
        if is_expired:
            return Response(AppResponse('Refresh token is expired').body())
        
        user = get_user_model().objects.get(pk=user_id)
        access_token = generate_access_token(user)
        
        response = {
            'access_token': access_token,
        }
        
        return Response(AppResponse(response).body())
    except:
        return Response(AppResponse('Invalid refresh token').body())

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_token(request):
    access_token = request.data.get('access_token', None)
    refresh_token = request.data.get('refresh_token', None)
    token = access_token if access_token else refresh_token
    if token is None:
        return Response(AppResponse('Token is required').body())
    try:
        payload = decode_token(token, is_refresh_token=refresh_token is not None)
        user_id = payload['user_id']
        exp = payload['exp']
        is_expired = exp < datetime.datetime.now().timestamp()
        user = get_user_model().objects.get(pk=user_id)
        is_valid_token = user.is_active and not is_expired
        response = {
            'token_validity': is_valid_token,
        }
        return Response(AppResponse(response).body())
    except:
        raise exceptions.ValidationError(AppResponse('Invalid token').error_body())


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    User = get_user_model()
    username = request.data.get('username')
    password = request.data.get('password')
    response = Response()
    if (username is None) or (password is None):
        raise exceptions.AuthenticationFailed(AppResponse('Username and password required', True).error_body())


    user = User.objects.filter(username=username).first()
    if(user is None):
        raise exceptions.AuthenticationFailed(AppResponse('User not found', True).error_body())
    if (not user.check_password(password)):
        raise exceptions.AuthenticationFailed(AppResponse('Wrong password', True).error_body())


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