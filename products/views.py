import json

from django.http    import JsonResponse
from django.views   import View
from django.db      import IntegrityError

from .models        import Product, Image, Menu, Category, SubCategory

class MenuView(View):
    def post(self, request):
        data = json.loads(request.body)
        Menu.objects.create(
            name = data['name']
        )
        return JsonResponse({"message": "menu create"}, status=201)

    def get(self, request):
        
        menu = Menu.objects.get(id=request.GET.get('id'))
        product_list = []
        
        outcategories = menu.category_set.all()
        for category in outcategories:
            incategories = category.subcategory_set.all()
            for subcategory in incategories:
                products = subcategory.product_set.all()
                for product in products:
                    product_list.append({
                        'name'  : product.name,
                        'price' : product.price,
                        'img'   : product.image_set.get(product=product).img
                    })
        
        return JsonResponse({'name' : menu.name, 'content' : product_list}, status = 200)
    

class CategoryView(View):
    def post(self, request):
        data = json.loads(request.body)
        Category.objects.create(
            name = data['name'],
            menu = Menu.objects.get(id= data['menu_id']),
        )

        return JsonResponse({"message": "category create"}, status=201)

    def get(self, request):
        category     = Category.objects.get(id=request.GET.get('id'))
        incategories = category.subcategory_set.all()
        product_list = []

        for subcategory in incategories:
            products = subcategory.product_set.all()

            for product in products:
                product_list.append({
                    'name'  : product.name,
                    'price' : product.price,
                    'img'   : product.image_set.get(id=1)
                })

        return JsonResponse({'name' : category.name, 'content' : product_list}, status = 200)

class SubCategoryView(View):
    def post(self, request):
        data = json.loads(request.body)

        SubCategory.objects.create(
            name       = data['name'],
            category = Category.objects.get(id= data['category_id'])
        )

        return JsonResponse({"message": "subcategory create"}, status=201)

    def get(self, request):
        subcategory = SubCategory.objects.get(id =request.GET.get('id'))
        products = subcategory.product_set.all()
        product_list = []

        for product in products:
            product_list.append({
                'name' : product.name,
                'price' : product.price,
                'img' : product.image_set.get(id=1)
            })

        return JsonResponse({'name' : subcategory.name, 'content' : product_list}, status = 200)

class ProductView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            Product.objects.get(user=request.user)

            Product.objects.create(
                subcategory = SubCategory.objects.get(id=data['subcategory']),
                name                = data['name'],
                color               = data['color'],
                team                = data['team'],
                product_code        = data['product_code'],
                product_detail_info = data['product_detail_info'],
                price               = data['price'],
                created_at          = data['created_at'],
                type                = data['type']
            )

            return JsonResponse({'message' : 'CREATED'}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

        except IntegrityError:
            return JsonResponse({'message' : 'DUPLICATED_CODE'}, status = 400)

    def get(self, request):
        product = Product.objects.get(id=request.GET.get('id'))

        product_list = {
            'name'                  : product.name,
            'color'                 : product.color,
            'team'                  : product.team,
            'product_code'          : product.product_code,
            'number_of_selling'     : product.number_of_selling,
            'product_detail_info'   : product.product_detail_info,
            'price'                 : product.price,
            'created_at'            : product.created_at,
            'type'                  : product.type,
        }

        return JsonResponse({'result' : product_list}, status = 200)
    
class ImageView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            images = Product.objects.get(id=data['product_id']).image_set.create(
                img = data['img'],
            )

            return JsonResponse({'message' : 'CREATED'}, status = 201)

        except KeyError:
            JsonResponse({'message' : 'KEY_ERROR'}, status = 400)