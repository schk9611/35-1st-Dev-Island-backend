import json, bcrypt

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError

from users.models           import User
from users.validation       import validate_email, validate_password

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']
            password = data['password']

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

