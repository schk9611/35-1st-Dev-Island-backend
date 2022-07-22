from django.db.models import Q

from django.http  import JsonResponse
from django.views import View

from products.models import Product, Category, SubCategory

class ProductListView(View):
    def get(self, request, category):

        show_list    = request.GET.get('show', 'all')
        order_method = request.GET.get('sort_method', '-release_date')
        limit        = int(request.GET.get('limit', 10))
        offset       = int(request.GET.get('offset', 0))
        
        products     = []
        res_products = []

        if show_list == 'all':
            category_id = Category.objects.get(name=category).id
            products = Product.objects.filter(sub_category__category_id=category_id).order_by(order_method)
        else:
            sub_cate_id = SubCategory.objects.get(name=show_list).id
            products = Product.objects.filter(sub_category_id=sub_cate_id).order_by(order_method)

        for product in products[offset:offset+limit]:
            res_products.append({
                'id'          : product.id,
                'name'        : product.name,
                'description' : product.description,
                'price'       : product.price,
                'image_url'   : [image.image_url for image in product.productimage_set.all()],
                'release_date': product.release_date,
            })

        return JsonResponse({'RESULT':res_products})