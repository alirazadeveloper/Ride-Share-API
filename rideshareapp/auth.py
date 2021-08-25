from django.utils import timezone
import jwt
from django.conf import settings


def generate_access_token(user):
    exp = timezone.now() + timezone.timedelta(days=1)
    access_token_payload = {
        'user_id': user.id,
        'exp': str(exp),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256')
    return access_token.decode("utf-8"), exp
