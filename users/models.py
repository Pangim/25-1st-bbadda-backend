from django.db import models
from django.db.models.fields import DateTimeField

class User(models.Model):
    name          = models.CharField(max_length=45)
    account       = models.CharField(max_length=45, null=True)
    phone_number  = models.CharField(max_length=45)
    telephon      = models.CharField(max_length=45, null=True)
    password      = models.CharField(max_length=200, null=True)
    address       = models.CharField(max_length=200, null=True)
    email         = models.CharField(max_length=45, null=True)
    mileage       = models.IntegerField(default=0, null=True)
    gender        = models.BooleanField(null=True)
    foreign       = models.BooleanField(null=True)
    date_of_birth = models.DateField(null=True)
    create_at     = DateTimeField(auto_now_add=True)
    updated_at    = DateTimeField(auto_now=True)
