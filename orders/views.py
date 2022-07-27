import json, datetime, re

from django.http import JsonResponse

from django.views  import View
from requests      import JSONDecodeError
from orders.models import Order, OrderProduct
from carts.models import Cart
from users.utils   import signin_decorator

class OrderView(View): 
    @signin_decorator
    def get(self, request):
        try:
            order_num = re.sub(r'[^0-9]', '', str(datetime.datetime.now()))

            orders_list   = []
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
                            'id'              : order_product.id,
                            'product_img'     : [img.image_url for img in order_product.product.productimage_set.all()],
                            'product_name'    : order_product.product.name,
                            'product_price'   : order_product.product.price,
                            'totalprice'      : order_product.product.price * order_product.quantity,
                            'product_quantity': order_product.quantity
                        }
                    )

            return JsonResponse({'orders_list' : orders_list, 'products_list' : products_list}, status=200)
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSONDecoderError'}, status=400)

    @signin_decorator
    def patch(self, request):
        try:
            data = json.loads(request.body)
            order_id = data['order_id']

            order = Order.objects.get(id=order_id)
            order.order_status_id = 2
            order.save()
            
            return JsonResponse({'message' : 'CANCEL_ORDER'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSONDecoderError'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except Order.DoesNotExist:
            return JsonResponse({'message' : 'ORDER_DOES_NOT_EXIST'}, status=404)

    @signin_decorator
    def post(self,request):
        try:
            data  = json.loads(request.body)
            carts = Cart.objects.filter(id__in=data['cart_ids'])
            
            with transaction.atomic():
                order = Order.objects.create(
                    order_status_id = 1,
                    user_id         = request.user.id
                )
                order_product_list = [OrderProduct(
                    order_id                = order.id,
                    product_id              = cart.product_id,
                    quantity                = cart.quantity,
                    order_product_status_id = 1
                    )for cart in carts]
                
                OrderProduct.objects.bulk_create(order_product_list)

                Cart.objects.filter(user=request.user, id__in=data['cart_ids']).delete()
                return JsonResponse({"message" : "NEW_ORDER_CREATED"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'message':'JSONDecodeError'}, status=404)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
