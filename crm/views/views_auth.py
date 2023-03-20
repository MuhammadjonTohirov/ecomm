import datetime
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from crm.utils.utils import decode_token, generate_access_token
from helpers.responses import AppResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['refresh_token'],
        properties={
            'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='The refresh token to generate a new access token from.'),
        },
    ),
    operation_description='Generates a new access token using a valid refresh token.',
    responses={
        200: openapi.Response(description='The new access token was generated successfully.'),
        400: openapi.Response(description='The request was invalid or malformed.'),
        401: openapi.Response(description='The specified refresh token was expired, invalid or revoked.'),
        500: openapi.Response(description='There was an internal server error.'),
    },
)
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
        payload = decode_token(
            token, is_refresh_token=refresh_token is not None)
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
        raise exceptions.ValidationError(
            AppResponse('Invalid token').error_body())
