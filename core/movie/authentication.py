import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
# from django.contrib.auth.models import User
from .models import User


import jwt
from rest_framework.authentication import BaseAuthentication

class MyJWTAuthentication(BaseAuthentication):

    model = None

    def get_model(self):
        return User

    def authenticate(self, request):

        authorization_heaader = request.headers.get('Authorization')

        if not authorization_heaader:
            return None
        try:
            # header = 'Token xxxxxxxxxxxxxxxxxxxxxxxx'
            access_token = authorization_heaader.split(' ')[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')

        user = User.objects.filter(username=payload['username']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        return (user, None)