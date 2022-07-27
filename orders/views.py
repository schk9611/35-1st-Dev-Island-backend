import json, re

from requests      import JSONDecodeError

from django.http   import JsonResponse
from django.views  import View
from django.db     import transaction

from carts.models import Cart
from users.utils   import signin_decorator
from orders.models import Order, OrderProduct


class OrderView(View): 
    @signin_decorator
    def get(self, request):
        try:
            result = {
                'id'         : request.user.id,
                'user_name'  : request.user.first_name + ' ' + request.user.last_name,
                'orders_list': [
                    {
                        'id'          : order.id,
                        'order_number': re.sub(r'[^0-9]', '', str(order.created_at)) + str(order.id),
                        # 'order_total_price' : [sum+=sum for sum in Product.Object.filter()],
                        'products'    : [
                            {
                                'id'          : order_product.id,
                                'product_img' : order_product.product.productimage_set.all()[0].image_url,
                                'product_name': order_product.product.name,
                                'product_price' : order_product.product.price,
                                'quantity' : order_product.quantity,
                                'product_total_price' : order_product.product.price * order_product.quantity
                            } for order_product in order.orderproduct_set.all()
                        ]
                    } for order in Order.objects.filter(user_id=request.user.id)
                ]
            }

            return JsonResponse({'RESULT' : result}, status=200)
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSONDecoderError'}, status=400)