import datetime, re

from django.http import JsonResponse

from django.views  import View
from requests      import JSONDecodeError
from orders.models import Order, OrderProduct
from users.utils   import signin_decorator

class OrderView(View): 
    @signin_decorator
    def get(self, request):
        try:
            order_num = re.sub(r'[^0-9]', '', str(datetime.datetime.now()))

            orders = [
                {
                    'id' : order.id,
                    'products' : [
                        {
                            'id' : order_product.id
                        } for order_product in order.orderproduct_set.all()
                    ]
                } for order in Order.objects.filter() 
            ]

            return JsonResponse({'orders_list' : orders_list, 'products_list' : products_list}, status=200)
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSONDecoderError'}, status=400)
