from django.db    import models

class Menu(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "menus"

class Category(models.Model):
    name = models.CharField(max_length=45)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    class Meta:
        db_table = "categories"

class SubCategory(models.Model):
    name        = models.CharField(max_length=45)
    category    = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = "sub_categories"

class Product(models.Model):
    name                = models.CharField(max_length=45)
    color               = models.CharField(max_length=45)
    team                = models.CharField(max_length=45)
    product_code        = models.CharField(max_length=45)
    type                = models.CharField(max_length=45)
    product_detail_info = models.CharField(max_length=2000)
    number_of_selling   = models.IntegerField(default=0)
    price               = models.DecimalField(max_digits=15, decimal_places=3)
    created_at          = models.DateField()
    sub_category        = models.ForeignKey(SubCategory, on_delete=models.SET_NULL , null=True)

    class Meta:
        db_table = "products"

class Products_sizes(models.Model):
    quantity  = models.IntegerField(default=0, null=True)
    size      = models.ForeignKey('Size', on_delete=models.CASCADE)
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = "products_sizes"

class Size(models.Model):
    type    = models.CharField(max_length=45)
    value   = models.CharField(max_length=45)
    product = models.ManyToManyField(Product, through=Products_sizes, through_fields=('size', 'product'))

    class Meta:
        db_table = "sizes"

class Image(models.Model):
    image_url      = models.CharField(max_length=2000)
    information    = models.TextField(max_length=50000)
    product        = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = "images"