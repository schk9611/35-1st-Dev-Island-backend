from django.db.models import Q

from django.http  import JsonResponse
from django.views import View

from products.models import Product, Category, SubCategory

class ProductListView(View):
    def get(self, request, category):

        show_list    = request.GET.get('show', 'home_audio') # all, portable, homeaudio
        order_method = request.GET.get('sort_method', '-price') # price, -price,   release_date, -release_date
        limit        = int(request.GET.get('limit', 3)) # 한 페이지에 보여줄 양
        offset       = int(request.GET.get('offset', 0)) # 보내질 데이터의 시작

        sub_categories = Category.objects.get(name=category).subcategory_set.all()
        sub_category_ids = [sub_category.id for sub_category in sub_categories]
        
        products     = []
        res_products = []

        if show_list == 'all':
            products = Product.objects.filter(Q(sub_category_id=sub_category_ids[0]) | Q(sub_category_id=sub_category_ids[1])).order_by(order_method)
        elif show_list == 'portable':
            products = Product.objects.filter(sub_category_id=sub_category_ids[0]).order_by(order_method)
        elif show_list == 'home_audio':
            products = Product.objects.filter(sub_category_id=sub_category_ids[1]).order_by(order_method)

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