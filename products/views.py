import json

from django.http    import JsonResponse
from django.views   import View
from django.db      import IntegrityError

from .models        import Product, Image, Menu, Category, SubCategory, Size

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
            menu         = Menu.objects.get(id=request.GET.get("id"))
            product_list = []
            categories   = menu.category_set.all()
            
            product_list.append([{
                "name"      : product.name, 
                "price"     : product.price, 
                "image_url" : product.image_set.filter(product=product).first().image_url
                } 
                for category in categories
                for subcategory in category.subcategory_set.all() 
                for product in subcategory.product_set.all()
            ])
            
            return JsonResponse({"name" : menu.name, "content" : product_list}, status = 200)

        except Menu.DoesNotExist:
            return JsonResponse({"message" : "MENU_DOES_NOT_EXIST"}, status = 400)

        except Category.DoesNotExist:
            return JsonResponse({"message" : "CATEGORY_DOES_NOT_EXIST"}, status = 400)

        except SubCategory.DoesNotExist:
            return JsonResponse({"message" : "SUB_CATEGORY_DOES_NOT_EXIST"}, status = 400)

class CategoryView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            Category.objects.create(
                name = data["name"],
                menu = Menu.objects.get(id= data["menu_id"]),
            )

            return JsonResponse({"message" : "CREATED"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

    def get(self, request):
        try:
            category       = Category.objects.get(id=request.GET.get("id"))
            sub_categories = category.subcategory_set.all()
            product_list   = []

            product_list.append([{
                "name"      : product.name, 
                "price"     : product.price, 
                "image_url" : product.image_set.filter(product=product).first().image_url,
                } 
                for sub_category in sub_categories 
                for product in sub_category.product_set.all()
            ])

            return JsonResponse({"name" : category.name, "content" : product_list}, status = 200)

        except Category.DoesNotExist:
            return JsonResponse({"message" : "CATEGORY_DOES_NOT_EXIST"}, status = 400)

class SubCategoryView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            SubCategory.objects.create(
                name       = data["name"],
                category   = Category.objects.get(id= data["category_id"])
            )

            return JsonResponse({"message": "CREATED"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

    def get(self, request):
        try:
            sub_category = SubCategory.objects.get(id =request.GET.get("id"))
            products     = sub_category.product_set.all()
            product_list = []
            product_list.append([{
                "name"      : product.name,
                "price"     : product.price,
                "image_url" : product.image_set.filter(product=product).first().image_url
                }
                for product in products
                ])

            return JsonResponse({"name" : sub_category.name, "content" : product_list}, status = 200)

        except SubCategory.DoesNotExist:
            return JsonResponse({"message" : "SUB_CATEGORY_DOES_NOT_EXIST"}, status = 400)

class ProductView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            Product.objects.create(
                sub_category        = SubCategory.objects.get(id=data["sub_category"]),
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
                "image"                 : [{"image_url_url" : image.image_url} for image in product.image_set.all()],
                "size"                  : {"value" : [size.value for size in product.size_set.all()]}
            }

            return JsonResponse({"result" : product_list}, status = 200)
    
        except Product.DoesNotExist:
            return JsonResponse({"message" : "PRODUCT_DOES_NOT_EXIST"}, status = 400)

class ImageView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            Product.objects.get(id=data['id']).image_set.create(
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
            data = json.loads(request.body)

            if Product.objects.get(id=data['product']).subcategory.category.menu.name != data['type']:
                return JsonResponse({"message" : "INVALID_SIZE_TYPE"})

            sizes = Size.objects.create(
                type  = data['type'],
                value = data['value'],
            )
            
            sizes.products_sizes_set.create(
                product = Product.objects.get(id=data['product']),
                size    = sizes,
            )
        
            return JsonResponse({"message" : "CREATED"}, status = 201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

        except Product.DoesNotExist:
            return JsonResponse({"message" : "PRODUCT_DOES_NOT_EXIST"}, status = 400)