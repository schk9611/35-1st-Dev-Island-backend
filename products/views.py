import json

from django.http       import JsonResponse
from django.views      import View

from products.models   import Product
class DetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id = product_id)
            product_list = {
                'name'       : product.id,
                'description': product.description,
                'content_url': product.content_url,
                'price'      : product.price,
                'stock'      : product.stock
            }
            return JsonResponse({"result" : product_list}, status=200)
        
        except Product.DoesNotExist:
            return JsonResponse({"message" : "DoesNotExist"}, status=400)
