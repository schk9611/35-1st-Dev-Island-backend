import json

from json.decoder import JSONDecodeError

from django.http import JsonResponse
from django.views import View

from products.models import Product, Category, SubCategory

class ProductListView(View):
    def get(self, request, category):
        """
        data = jsob....

        {
            "email" : "abc",
            "password" : "123"
        }

        email = data['email']
        password = data['password1']

        data.get('password1') -> None
        """
        
        # sort_by = list(request.GET.get('sorted', 'release_date'))
        # show = list(request.GET.get('show', 10))


        # product_list = Product.objects.all().order_by(sort_by)
        # paginator = Paginator(product_list, show)

        # page_number = list(request.GET.get('page'))
        # page_obj = paginator.get_page(page_number)
        # return JsonResponse({'RESULT': page_obj}, status=200)

        """
        category, subcategory를 한개씩 확인하고 들어가는 과정이 필요하다.
        """        

        order_method = request.GET.get('sort_method', 'release_date')
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))

        # sort_dict = {
        #     'a' : '-price',
        #     'b' : 'price'
        # }

        sub_categories = Category.objects.get(name=category).subcategory_set.all()

        sub_category_ids = [sub_category.id for sub_category in sub_categories]
        
        products = []
        res_products = []

        for sub_category_id in sub_category_ids:
            products = Product.objects.filter(sub_category_id=sub_category_id).order_by(order_method)
            for product in products:
                res_products.append(product)
            products=[]
        
        # if order_method == 0:
        #     product_all = Product.objects.all()[offset:offset+limit]
        # elif order_method == 1:
        #     product_all = Product.objects.order_by('price')[offset:offset+limit]
        # elif order_method == 2:
        #     product_all = Product.objects.order_by('-price')[offset:offset+limit]
        # elif order_method == 3:
        #     product_all = Product.objects.order_by('release_date')[offset:offset+limit]
        # elif order_method == 4:
        #     product_all = Product.objects.order_by('-release_date')[offset:offset+limit]
        
        result = []

        for product in res_products:
            result.append({
                'id' : product.id,
                'name' : product.name,
                'description' : product.description,
                'price' : product.price,
                'image_url' : [image.image_url for image in product.productimage_set.all()],
                'release_date' : product.release_date,
            })


        return JsonResponse({'RESULT':result})