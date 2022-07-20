import os
import django
import csv
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weolufsen.settings')
django.setup()

from products.models import Product, ProductImage, Category, SubCategory

CSV_PATH_PRODUCTS = 'csv/product.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    for row in data_reader:
        print(row)