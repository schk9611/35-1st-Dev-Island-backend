from django.http  import JsonResponse
from django.views import View

from products.models import Product, Category, SubCategory

class ProductListView(View):
    def get(self, request, category):

        order_method = request.GET.get('sort_method', 'release_date')
        limit        = int(request.GET.get('limit', 10))
        offset       = int(request.GET.get('offset', 0))

        sub_categories   = Category.objects.get(name=category).subcategory_set.all()
        sub_category_ids = [sub_category.id for sub_category in sub_categories]
        
        products     = []
        res_products = []

        for sub_category_id in sub_category_ids:
            products = Product.objects.filter(sub_category_id=sub_category_id).order_by(order_method)
            for product in products:
                res_products.append(product)
            products=[]
        
        result = []

        for product in res_products:
            result.append({
                'id'          : product.id,
                'name'        : product.name,
                'description' : product.description,
                'price'       : product.price,
                'image_url'   : [image.image_url for image in product.productimage_set.all()],
                'release_date': product.release_date,
            })

        return JsonResponse({'RESULT':result})