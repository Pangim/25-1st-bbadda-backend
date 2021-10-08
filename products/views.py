import json

from django.http    import JsonResponse
from django.views   import View
from django.db      import IntegrityError

from .models        import Product, Image, Menu, Category, Sub_category

class MenuView(View):
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
            menu = Menu.objects.get(id=request.GET.get("id"))
            product_list = []
            categories = menu.category_set.all()
            for category in categories:
                product_list = [{"name" : j.name, "price" : j.price, "img" : j.img} 
                                for i in category.sub_category_set.all() 
                                for j in i.product_set.all()]
            
            return JsonResponse({"name" : menu.name, "content" : product_list}, status = 200)

        except Menu.DoesNotExist:
            return JsonResponse({"message" : "MENU_DOES_NOT_EXIST"}, status = 400)

class CategoryView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            Category.objects.create(
                name = data["name"],
                menu = Menu.objects.get(id= data["menu_id"]),
            )

            return JsonResponse({"message": "CREATED"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "CREATED"}, status = 400)

    def get(self, request):
        try:
            category       = Category.objects.get(id=request.GET.get("id"))
            sub_categories = category.sub_category_set.all()
            product_list   = []

            for sub_category in sub_categories:
                products = sub_category.product_set.all()

                for product in products:
                    product_list.append({
                        "name"  : product.name,
                        "price" : product.price,
                        "img"   : product.image_set.get(id=1)
                    })

            return JsonResponse({"name" : category.name, "content" : product_list}, status = 200)

        except Category.DoesNotExist:
            return JsonResponse({"message" : "CATEGORY_DOES_NOT_EXIST"}, status = 400)

class Sub_categoryView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            Sub_category.objects.create(
                name       = data["name"],
                category = Category.objects.get(id= data["category_id"])
            )

            return JsonResponse({"message": "CREATED"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

    def get(self, request):
        try:
            sub_category = Sub_category.objects.get(id =request.GET.get("id"))
            products = sub_category.product_set.all()
            product_list = []

            for product in products:
                product_list.append({
                    "name" : product.name,
                    "price" : product.price,
                    "img" : product.image_set.get(id=1)
                })

            return JsonResponse({"name" : sub_category.name, "content" : product_list}, status = 200)

        except Sub_category.DoesNotExist:
            return JsonResponse({"message" : "SUB_CATEGORY_DOES_NOT_EXIST"}, status = 400)

class ProductView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            Product.objects.create(
                sub_category        = Sub_category.objects.get(id=data["sub_category"]),
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

        except Sub_category.DoesNotExist:
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
                "image"                 : [{"img_url" : i.img} for i in product.image_set.all()],
                "size"                  : {"value" : [i.value for i in product.size_set.all()]}
            }

            return JsonResponse({"result" : product_list}, status = 200)
    
        except Product.DoesNotExist:
            return JsonResponse({"message" : "PRODUCT_DOES_NOT_EXIST"}, status = 400)

class ImageView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            Product.objects.get(id=data["id"]).image_set.create(
                img = data["img"],
            )

            return JsonResponse({"message" : "CREATED"}, status = 201)

        except KeyError:
            JsonResponse({"message" : "KEY_ERROR"}, status = 400)