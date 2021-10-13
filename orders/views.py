import json
import random

from django.views    import View
from django.http     import JsonResponse

from users.models    import User
from orders.models   import Order
from products.models import Product, Size
from utils           import login_required

class OrderView(View):
        @login_required
        def post(self, request):
            try:
                data              = json.loads(request.body)
                user              = request.user
                type              = data['type']
                value             = data['value']
                quantity          = data['quantity']
                products          = Product.objects.get(product_code = request.GET.get('code'))
                products_filter   = Size.objects.get(type=type, value=value).products_sizes_set.filter(product = products)

                if user.point - int(quantity) * products.price < 0:
                    return JsonResponse({"message":"NO MONEY"}, status=401)

                if products_filter.first().quantity - int(quantity) < 0:
                    return JsonResponse({"message":"NO PRODUCT"}, status=401)

                if products_filter.exists():
                    
                    products_filter.update(quantity=products_filter.first().quantity-int(quantity))
                    products.number_of_selling += int(quantity)
                    products.save()
                    user.address = data['address']
                    user.point = user.point - products.price
                    user.save()

                    order_number = str(user.id)+str(request.GET.get('code')) +str(random.randrange(100000,999999))
                    
                    Order.objects.create(
                        receiver_name           = data['receiver_name'],
                        receiver_mobile_number  = data['receiver_mobile_number'],
                        receiver_address        = data['receiver_address'],
                        request                 = data['request'],
                        order_number            = order_number,
                        user_id                 = user.id
                    )

                    return JsonResponse({"massage":"create"}, status=201)
            
            except KeyError:
                return JsonResponse({"massage":"KeyError"}, status=401)

        @login_required
        def get(self, request):
            try:
                user = request.user.id
                user_name          = User.objects.get(id = user).name
                user_mobile_number = User.objects.get(id = user).mobile_number
                user_email         = User.objects.get(id = user).email

                user_information = {
                    "name"          : user_name,
                    "mobile_number" : user_mobile_number,
                    "email"         : user_email
                }


                return JsonResponse({"User" : user_information}, status=201)

            except KeyError:
                return JsonResponse({"massage" : "KeyError"}, status=401)
