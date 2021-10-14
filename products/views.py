import json

from django.http      import JsonResponse
from django.views     import View
from django.db        import IntegrityError
from django.db.models import Q

from .models          import Product, Image, Menu, Category, SubCategory, Size

class ProductsView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            Menu.objects.create(
                name = data["name"]
            )

            return JsonResponse({"message": "CREATED"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

    def get(self, request):
        try:
            menu_name    = request.GET.get('name')
            sorting      = request.GET.get('sort', '-created_at')
            offset       = int(request.GET.get('offset', 0))
            limit        = int(request.GET.get('limit', 8))
            menu         = Menu.objects.filter(name=menu_name)
            category     = Category.objects.filter(name=menu_name)
            sub_category = SubCategory.objects.filter(name=menu_name)
            q            = Q()

            menu_list = [menu, category, sub_category]
            for menus in menu_list:
                if menus:
                    menu = menus.first()

            if menu:
                products = menu.product_set.filter().order_by(sorting)[offset:offset+limit]

            else:
                products = Product.objects.all().order_by(sorting)[0:4]

            product_list = [{
                "id"                : product.id,
                "menu_name"         : product.menu.name,
                "category_name"     : product.category.name,
                "sub_category_name" : product.sub_category.name,
                "name"              : product.name, 
                "price"             : product.price, 
                "image_url"         : {"image_url1" :product.image_set.first().image_url, "image_url2" :product.image_set.last().image_url} 
                                        if product.image_set.first() and product.image_set.last() else None,
                "created_at"        : product.created_at,
                "number_of_selling" : product.number_of_selling,
                "url"               : "/products/product?id={}".format(product.id)
                } 
                for product in products
            ]
                        
            return JsonResponse({"content" : product_list}, status = 200)
            
            

        except Menu.DoesNotExist:
            return JsonResponse({"message" : "MENU_DOES_NOT_EXIST"}, status = 400)

        except Category.DoesNotExist:
            return JsonResponse({"message" : "CATEGORY_DOES_NOT_EXIST"}, status = 400)

        except SubCategory.DoesNotExist:
            return JsonResponse({"message" : "SUB_CATEGORY_DOES_NOT_EXIST"}, status = 400)
  

class ProductView(View):
    def post(self, request):
        try:
            data          = json.loads(request.body)
            menu          = Menu.objects.get(id=data['menu'])
            category      = menu.category_set.get(id=data['category'])
            sub_category  = category.subcategory_set.get(id=data['sub_category'])
            Product.objects.create(
                menu                = menu,
                category            = category,
                sub_category        = sub_category,
                name                = data["name"],
                color               = data["color"],
                team                = data["team"],
                product_code        = data["product_code"],
                product_detail_info = data["product_detail_info"],
                information         = data["information"],
                price               = data["price"],
                created_at          = data["created_at"],
            )

            return JsonResponse({"message" : "CREATED"}, status = 201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

        except Menu.DoesNotExist:
            return JsonResponse({'message' : "MENU_DOES_NOT_EXIST"}, status = 400)

        except Category.DoesNotExist:
            return JsonResponse({'message' : "CATEGORY_DOES_NOT_EXIST"}, status = 400)

        except SubCategory.DoesNotExist:
            return JsonResponse({"message" : "SUB_CATEGORY_DOES_NOT_EXIST"}, status = 400)

        except IntegrityError:
            return JsonResponse({"message" : "DUPLICATED_CODE"}, status = 400)

    def get(self, request):
        try:
            product = Product.objects.get(id=request.GET.get("id"))
            product_list = {
                "name"                  : product.name,
                "color"                 : product.color,
                "team"                  : product.team,
                "product_code"          : product.product_code,
                "product_detail_info"   : product.product_detail_info,
                "information"           : product.information,
                "price"                 : product.price,
                "created_at"            : product.created_at,
                "img"                 : [{"img_url" : image.image_url} for image in product.image_set.all()],
                "size"                  : [{
                    "type"     : size.type, 
                    "value"    : size.value, 
                    "quantity" : size.products_sizes_set.first().quantity} for size in product.size_set.all()]
            }

            return JsonResponse({"result" : product_list}, status = 200)
    
        except Product.DoesNotExist:
            return JsonResponse({"message" : "PRODUCT_DOES_NOT_EXIST"}, status = 400)

class ImageView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            Product.objects.get(id=data['product_id']).image_set.create(
                image_url = data["image_url"],
            )

            return JsonResponse({"message" : "CREATED"}, status = 201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

        except Product.DoesNotExist:
            return JsonResponse({"message" : "PRODUCT_DOES_NOT_EXIST"}, status = 400)

class SizeView(View):
    def post(self, request):
        try:
            data  = json.loads(request.body)
            sizes = Size.objects.get(id=data['size'])

            if Product.objects.get(id=data['product']).menu.name != sizes.type:
                return JsonResponse({"message" : "INVALID_SIZE_TYPE"})

            sizes = Size.objects.create(
                type  = data['type'],
                value = data['value'],
            )
        
            return JsonResponse({"message" : "CREATED"}, status = 201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

        except Product.DoesNotExist:
            return JsonResponse({"message" : "PRODUCT_DOES_NOT_EXIST"}, status = 400)