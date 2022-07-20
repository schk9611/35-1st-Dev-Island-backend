import json
from math import ceil

from json.decoder import JSONDecodeError

from django.http import JsonResponse
from django.views import View

from products.models import Product
from users.models import User

class ProductListView(View):
    def get(self, request):
        # sort_by = list(request.GET.get('sorted', 'release_date'))
        # show = list(request.GET.get('show', 10))


        # product_list = Product.objects.all().order_by(sort_by)
        # paginator = Paginator(product_list, show)

        # page_number = list(request.GET.get('page'))
        # page_obj = paginator.get_page(page_number)
        # return JsonResponse({'RESULT': page_obj}, status=200)

        order_method = int(request.GET.get('sort_method', None))
        limit = int(request.GET.get('limit', 0))
        offset = int(request.GET.get('offset', 0))

        if order_method == 0:
            product_all = Product.objects.all()[offset:offset+limit]
        elif order_method == 1:
            product_all = Product.objects.order_by('price')[offset:offset+limit]
        elif order_method == 2:
            product_all = Product.objects.order_by('-price')[offset:offset+limit]
        elif order_method == 3:
            product_all = Product.objects.order_by('release_date')[offset:offset+limit]
        elif order_method == 4:
            product_all = Product.objects.order_by('-release_date')[offset:offset+limit]

        return JsonResponse({'RESULT':product_all})