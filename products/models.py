from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'categories'

class SubCategory(models.Model):
    name     = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categories'

class Product(models.Model):
    name         = models.CharField(max_length=100)
    description  = models.CharField(max_length=500)
    content_url  = models.CharField(max_length=200)
    price        = models.DecimalField(max_digits=6, decimal_places=2)
    stock        = models.IntegerField()
    release_date = models.DateField()
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'

class ProductImage(models.Model):
    image_url = models.CharField(max_length=200)
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_images'



