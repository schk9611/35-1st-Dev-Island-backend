import json
import re

import bcrypt
import jwt
from django.http            import JsonResponse
from django.core.exceptions import ValidationError
from django.views           import View
from django.conf            import settings

from users.models     import User
from users.validation import validate_email, validate_password

class SignUpView(View):
    def post(self, request):
        try:
            data       = json.loads(request.body)
            first_name = data['first_name']
            last_name  = data['last_name']
            email      = data['email']
            password   = data['password']

            validate_email(email)
            validate_password(password)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message" : "THIS_EMAIL_ALREADY_EXISTS"}, status=400)
            
            hashed_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')

            User.objects.create(
                first_name = first_name,
                last_name  = last_name,
                email      = email,
                password   = hashed_password
            )

            return JsonResponse({"message" : "SIGNUP_SUCCESS"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"message" : "JSONDecodeError"}, status=404)
    
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

        except ValidationError as error:
            return JsonResponse({"message" : error.message}, status=400)

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
