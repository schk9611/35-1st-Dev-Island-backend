import json
import jwt

from django.http import JsonResponse
from django.conf import settings

from users.models import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get()
            payload = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)
            user = User.objects.get(id=payload['id'])
            request.user = user