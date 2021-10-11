import json
import bcrypt
import jwt

from django.views   import View
from django.http    import JsonResponse
from django.db      import IntegrityError

from .models        import User
from my_settings    import SECRET_KEY, ALGORITHM
from .validation    import validate_email, validate_password


class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(account=data['account']).exists():
                return JsonResponse({'message' : 'DUPLICATED_ID'}, status = 400)

            if not validate_email(data['email']):
                return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)

            if not validate_password(data['password']):
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

            User.objects.create(
                name             = data['name'],
                account          = data['account'],
                password         = hashed_password.decode('utf-8'),
                date_of_birth    = data.get('date_of_birth'),
                gender           = data['gender'],
                foreigner        = data['foreigner'],
                mobile_number    = data['mobile_number'],
                email            = data['email'],
                telephone_number = data.get('telephone_number'),
                address          = data.get('address'),
            )

            return JsonResponse({'message' : 'CREATED'}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

class SigninView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            account  = data['account']
            password = data['password']
            user = User.objects.get(account=account)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)
            
            token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm=ALGORITHM)

            return JsonResponse({'message' : 'SUCCESS', 'access_token' : token}, status = 200)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_ID'}, status = 400)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
            