from django.db       import models

class Menu(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "menus"

class OutCategory(models.Model):
    name = models.CharField(max_length=45)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    class Meta:
        db_table = "outcategories"

class InCategory(models.Model):
    name        = models.CharField(max_length=45)
    outcategory = models.ForeignKey(OutCategory, on_delete=models.CASCADE)

    class Meta:
        db_table = "incategories"
