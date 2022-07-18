import json
import re

import bcrypt
import jwt
from django.http import JsonResponse
from django.views import View
from django.conf import settings

from users.models import User

class LogInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(email=data['email'])

            if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message':'INVALID_USER'}, status=401)

            access_token = jwt.encode({'id': user.id}, settings.SECRET_KEY, settings.ALGORITHM)

            return JsonResponse({'message':'SUCCESS', 'ACCESS_TOKEN':access_token}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'message':'JSONDecodeError'}, status=404)
        except User.DoesNotExist:
            return JsonResponse({'message':'DoesNotExist'}, status=404)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)