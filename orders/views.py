import json
import random

from django.views    import View
from django.http     import JsonResponse

from orders.models   import Order, Order_status_code
from products.models import Product
from users.models    import User
from utils           import login_required

class OrderView(View):
        def post(self, request):
            # try:
                data           = json.loads(request.body)

                products       = Product.objects.get(product_code = request.GET.get('code'))
                products_sizes = products.products_sizes_set.all()

                User.objects.create(
                    name          = data['name'],
                    mobile_number = data['mobile_number'],
                    email         = data['email'],
                    address       = data['address'],
                )

                user_id = User.objects.last().id
                order_number = str(user_id)+ str(random.randrange(100000,999999))
                
                Order.objects.create(
                    receiver_name           = data['receiver_name'],
                    receiver_mobile_number  = data['receiver_mobile_number'],
                    receiver_address        = data['receiver_address'],
                    request                 = data['request'],
                    order_number            = order_number,
                    user_id                 = user_id
                )

                # if products_sizes.objects.filter()

                return JsonResponse({"massage":"create"}, status=201)
            
            # except KeyError:
            #     return JsonResponse({"massage":"KeyError"}, status=401)

        @login_required
        def get(self, request):
            try:
                user = request.user.id
                user_name          = User.objects.get(id = user).name
                user_mobile_number = User.objects.get(id = user).mobile_number
                user_email         = User.objects.get(id = user).email
                # quantity = request.GET.get('quantity')

                # products           = Product.objects.get(product_code = request.Get.get('code'))
                # products_sizes     = products.products_sizes_set.all()
                # products_images     = products.images_set.all()
                # sizes              = products_sizes.sizes_set.all()

                user_information = [{
                    "name"          : user_name,
                    "mobile_number" : user_mobile_number,
                    "email"         : user_email,
                }]

                # products_information = [{
                #     "name"     : products.name,
                #     "size"     : sizes.value,
                #     "price"    : products.price,
                #     "image"    : products_images.image_url,
                #     "quantity" : quantity
                # }]

                return JsonResponse({"User" : user_information}, status=201)
#, "Product" : products_information
            except KeyError:
                return JsonResponse({"massage" : "KeyError"}, status=401)
