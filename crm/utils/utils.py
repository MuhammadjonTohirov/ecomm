import datetime
import jwt
from django.conf import settings

from e_commerce.settings import REFRESH_TOKEN_SECRET

def decode_token(token, is_refresh_token=False):
    try:
        key = settings.REFRESH_TOKEN_SECRET if is_refresh_token else settings.SECRET_KEY
        return jwt.decode(token, key, algorithms=['HS256'])
    except:
        return None

def generate_access_token(user):
    access_token_payload = {
        'user_id': user.id, 
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=50),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256')#.decode('utf-8')
    return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.REFRESH_TOKEN_SECRET, algorithm='HS256')#.decode('utf-8')

    return refresh_token