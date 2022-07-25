from django.http  import JsonResponse
from django.views import View

from products.models import Product, Category, SubCategory

class ProductListView(View):
    def get(self, request):
        try:
            category    = request.GET.get('category', 'speakers')
            show        = request.GET.get('show', 'all')
            sort_method = request.GET.get('sort_method', '-release_date')
            limit       = int(request.GET.get('limit', 9))
            offset      = int(request.GET.get('offset', 0))

            if show == 'all':
                category_id = Category.objects.get(name=category).id
                products    = Product.objects.filter(sub_category__category_id=category_id).order_by(sort_method)
            else:
                sub_cate_id = SubCategory.objects.get(name=show).id
                products    = Product.objects.filter(sub_category_id=sub_cate_id).order_by(sort_method)

            res_products = [{
                    'id'          : product.id,
                    'name'        : product.name,
                    'description' : product.description,
                    'price'       : product.price,
                    'image_url'   : [image.image_url for image in product.productimage_set.all()],
                    'release_date': product.release_date,
                } for product in products[offset:offset+limit]] 

            return JsonResponse({'RESULT':res_products, 'totalItems' : products.count()}, status=200)
        
        except Category.DoesNotExist:
            return JsonResponse({'message':'CATEGORY_DOES_NOT_EXIST'}, status=400)
        except SubCategory.DoesNotExist:
            return JsonResponse({'message':'SUB_CATEGORY_DOES_NOT_EXIST'}, status=400)

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