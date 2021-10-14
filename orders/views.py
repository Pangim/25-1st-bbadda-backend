import json
import random

from django.views    import View
from django.http     import JsonResponse
from django.db       import transaction

from users.models    import User
from orders.models   import Order, Order_item, Users_Products
from products.models import Product, Size, Image
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
                user_product      = Users_Products.objects.get(user=user)
                products          = Product.objects.get(id=user_product.products_sizes.product.id)
                products_filter   = Size.objects.get(type=type, value=value).products_sizes_set.filter(product = products)

                if user.point - (int(quantity) * products.price) < 0:
                    return JsonResponse({"message":"NOT ENOUGH MONEY"}, status=401)

                if products_filter.first().quantity - int(quantity) < 0:
                    return JsonResponse({"message":"QUANTITY EXCEEDED"}, status=401)

                if products_filter.exists():
                    with transaction.atomic():

                        order_number = str(user.id)+str(request.GET.get('code')) +str(random.randrange(100000,999999))
                        
                        order = Order.objects.create(
                            receiver_name           = data['receiver_name'],
                            receiver_mobile_number  = data['receiver_mobile_number'],
                            receiver_address        = data['address'],
                            request                 = data['request'],
                            order_number            = order_number,
                            user_id                 = user.id
                        )

                        Order_item.objects.create(
                            order      = order,
                            size_type  = user_product.products_sizes.size.type,
                            size_value = user_product.products_sizes.size.value,
                            quantity   = quantity,
                            product    = products,
                        )

                        products_filter.update(quantity=products_filter.first().quantity-int(quantity))
                        products.number_of_selling += int(quantity)
                        products.save()
                        user.address = data['address']
                        user.point   = user.point - products.price
                        user.save()

                        return JsonResponse({"massage":"create"}, status=201)
            
            except KeyError:
                return JsonResponse({"massage":"KeyError"}, status=401)

        @login_required
        def get(self, request):
            try:
                user               = request.user
                user_name          = User.objects.get(id = user.id).name
                user_mobile_number = User.objects.get(id = user.id).mobile_number
                user_product       = Users_Products.objects.get(user=user)
                user_email         = User.objects.get(id = user.id).email
                products           = Product.objects.get(id=user_product.products_sizes.product.id)
                image              = Image.objects.filter(product_id = products.id).first()
                allprice           = user_product.quantity * int(products.price)

                user_information = {
                    "name"          : user_name,
                    "mobile_number" : user_mobile_number,
                    "email"         : user_email,
                    "product"       : products.name,
                    "price"         : int(products.price),
                    "img"           : image.image_url if image else None,
                    "quantity"      : user_product.quantity,
                    "value"         : user_product.products_sizes.size.value,
                    "type"          : user_product.products_sizes.size.type,
                    "allprice"      : allprice,
                    "point"         : int(user.point)
                }

                return JsonResponse({"User" : user_information}, status=200)

            except KeyError:
                return JsonResponse({"massage" : "KeyError"}, status=401)

        @login_required
        def delete(self,request):
            user         = request.user
            Users_Products.objects.get(user=user).delete()

            return JsonResponse({"message":"DELETED"}, status=204)

class OrderProductView(View):
    @login_required
    def post(self,request):
        try:
            data           = json.loads(request.body)
            user           = request.user
            products       = Product.objects.get(product_code = data['product_code'])
            quantity       = data['selectedQuantity']
            sizes          = Size.objects.get(type=data['size_type'], value=data['selected_size_value'])
            products_sizes = products.products_sizes_set.get(size= sizes)

            Users_Products.objects.create(
                products_sizes = products_sizes,
                user           = user,
                quantity       = quantity
            )
            return JsonResponse({"message":"create"}, status=201)

        except KeyError:
            return JsonResponse({"message":"KEYERROR"}, status=401)

