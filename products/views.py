from itertools import product
import json
from json.decoder import JSONDecodeError

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views import View

from products.models import Product
from users.models import User

class ProductListView(View):
    def get(self, request):
        # 
        sort_by = request.GET.get('sorted', 'release_date')
        show = request.GET.get('show', 10)


        product_list = Product.objects.all().order_by(sort_by)
        paginator = Paginator(product_list, show)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return JsonResponse({'RESULT': page_obj}, status=200)