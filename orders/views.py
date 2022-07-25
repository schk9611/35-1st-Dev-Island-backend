import datetime, re

from django.http import JsonResponse

from django.views  import View
from orders.models import Order, OrderProduct
from users.models import User
from users.utils   import signin_decorator

class OrderView(View): 
    @signin_decorator
    def get(self, request): 
        order_num = re.sub(r'[^0-9]', '', str(datetime.datetime.now()))

        orders_list = []
        products_list = []

        for order in Order.objects.filter(user=request.user):
            orders_list.append(
                {
                    'id' : order.id,
                    'order_num' : order_num,
                    'user_name' : order.user.first_name + ' ' + order.user.last_name,
                }
            )
            for order_product in OrderProduct.objects.filter(order_id=order.id):
                products_list.append(
                    {
                        'id' : order_product.id,
                        'product_img' : [product_image for product_image in order_product.product.productimage_set.all()],
                        'product_name' : order_product.product.name,
                        'product_price' : order_product.product.price * order_product.quantity,
                        'product_quantity' : order_product.quantity
                    }
                )

        # orders_list = [
        #     {
        #         'id'       : order.id,
        #         'order_num': order_num,
        #         'user_name': order.user.first_name + order.user.last_name
        #     } for order in Order.objects.filter(user=request.user)
        # ]
        # print(orders_list)

        # products_list = [
        #     {
        #         'id'              : order_product.id,
        #         'product_img'     : order_product.product.productimg_set.image_url,
        #         'product_name'    : order_product.product.name,
        #         'product_price'   : order_product.product.price * order_product.quantity,
        #         'product_quantity': order_product.quantity,
        #     } for order_product in OrderProduct.objects.filter(order_id=)
        # ]
        # print(products_list)

        return JsonResponse({'orders_list' : orders_list, 'products_list' : products_list}, status=200)
