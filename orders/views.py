import re

from django.http import JsonResponse

from django.views  import View
from requests      import JSONDecodeError
from orders.models import Order, OrderProduct
from users.utils   import signin_decorator

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

            
                # for order_product in OrderProduct.objects.filter(order_id=order.id):
                #     products_list.append(
                #         {
                #             'id'              : order_product.id,
                #             'product_img'     : [img.image_url for img in order_product.product.productimage_set.all()],
                #             'product_name'    : order_product.product.name,
                #             'product_price'   : order_product.product.price,
                #             'totalprice'      : order_product.product.price * order_product.quantity,
                #             'product_quantity': order_product.quantity
                #         }
                #     )

            return JsonResponse({'RESULT' : result}, status=200)
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSONDecoderError'}, status=400)