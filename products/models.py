from django.db    import models

from menus.models import InCategory

class Product(models.Model):
    name                = models.CharField(max_length=45)
    color               = models.CharField(max_length=45)
    team                = models.CharField(max_length=45)
    product_code        = models.CharField(max_length=45)
    type                = models.CharField(max_length=45)
    product_detail_info = models.CharField(max_length=2000)
    number_of_selling   = models.IntegerField(default=0)
    price               = models.DecimalField(max_digits=15, decimal_places=3)
    create_at           = models.DateField()
    incategory          = models.ForeignKey(InCategory, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "products"

class Products_sizes(models.Model):
    quantity  = models.IntegerField(default=0, null=True)
    size      = models.ForeignKey(Size, on_delete=models.CASCADE)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = "products_sizes"

class Size(models.Model):
    type    = models.CharField(max_length=45)
    value   = models.CharField(max_length=45)
    product = models.ManyToManyField(Product, through=Products_sizes, through_fields=('products', 'sizes'))

    class Meta:
        db_table = "sizes"

class Image(models.Model):
    url      = models.CharField(max_length=2000)
    info_img = models.TextField(max_length=50000)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = "images"