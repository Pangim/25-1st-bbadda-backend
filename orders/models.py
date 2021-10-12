from django.db          import models

from users.models       import User
from products.models    import Product
from core.models        import TimeStampModel

class Order_item_status_code(models.Model):
    order_item_status_code          = models.CharField(max_length=45)
    order_item_status_description   = models.CharField(max_length=200)

    class Meta:
        db_table = 'order_item_status_codes'

class Order_status_code(models.Model):
    order_status_code           = models.CharField(max_length=45)
    order_status_description    = models.CharField(max_length=200)
    order                       = models.ForeignKey("Order", on_delete=models.CASCADE)

    class Meta:
        db_table = 'order_status_codes'

class Order(TimeStampModel):
    receiver_name           = models.CharField(max_length=45)
    receiver_mobile_number  = models.CharField(max_length=45)
    order_number            = models.CharField(max_length=45)
    receiver_address        = models.CharField(max_length=200)
    request                 = models.CharField(max_length=2000)
    user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    product                 = models.ManyToManyField(Product, through='Order_item', through_fields=('order','product'))
    
    class Meta:
        db_table = 'orders'

class Order_item(models.Model):
    size_type                 = models.CharField(max_length=45)
    size_value                = models.CharField(max_length=45)
    quantity                  = models.IntegerField()
    product                   = models.ForeignKey(Product, on_delete=models.CASCADE)
    order                     = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_item_status_code    = models.ForeignKey(Order_item_status_code, on_delete=models.CASCADE)

    class Meta:
        db_table = 'order_items'

class Shipment(TimeStampModel):
    shipment_tracking_number    = models.CharField(max_length=45)
    order_shipment_detail       = models.CharField(max_length=200)
    shipment_date               = models.DateField()
    order                       = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'shipments'