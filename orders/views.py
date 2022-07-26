import json

from django.http     import JsonResponse
from django.views    import View
from django.db       import transaction

from carts.models    import Cart
from users.utils     import signin_decorator
from orders.models   import Order, OrderProduct


class OrderView(View):
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