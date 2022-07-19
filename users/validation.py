import re

from django.http            import JsonResponse
from django.core.exceptions import ValidationError

EMAIL_REGEX    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
PASSWORD_REGEX = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[?!@#$%*&])[A-Za-z\d?!@#$%*&]{8,}$'

def validate_email(email):
    if not re.match(EMAIL_REGEX, email):
        raise ValidationError('INVALID_EMAIL')

def validate_password(password):
    if not re.match(PASSWORD_REGEX, password):
        raise ValidationError('INVALID_PASSWORD')