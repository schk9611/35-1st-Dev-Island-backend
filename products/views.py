import json

from django.http       import JsonResponse
from django.views      import View

from products.models   import Product
class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id = product_id)
            product_detail = {
                'id'           : product.id,
                'name'         : product.name,
                'product_image': [product.image_url for product in product.productimage_set.all()],
                'description'  : product.description,
                'content_url'  : product.content_url,
                'price'        : product.price,
                'stock'        : product.stock
            }
            return JsonResponse({"result" : product_detail}, status=200)
        
        except Product.DoesNotExist:
            return JsonResponse({"message" : "DoesNotExist"}, status=400)
