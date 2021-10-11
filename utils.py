import jwt

from django.http import JsonResponse

from users.models import User
from my_settings import SECRET_KEY, ALGORITHM

def login_deco(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            user_info = jwt.decode(request.headers.get('authorization'), SECRET_KEY, algorithms=ALGORITHM)
            user = User.objects.get(id=user_info)
            request.user = user

        except User.DoesNotExist:
            return JsonResponse({'message' : 'USER_DOES_NOT_EXIST'}, status = 400)

        except jwt.DecodeError:
            return JsonResponse({'message' : 'KNOWN_USER'}, status = 400)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message' : 'EXPIRED_TOKEN'}, status = 400)

        return func(self, request, *args, **kwargs)

    return wrapper