import json
from django.http import JsonResponse

from django.views import View
from orders.models import Order, OrderProduct
from users.utils import signin_decorator
from carts.models import Cart

class OrderView(View):
    @signin_decorator
    def post(self, request):
        try:
            data     = json.loads(request.body)
            carts_id = data['carts_id']
            
            order = Order.objects.create(
                order_status_id = 1,
                user_id         = request.user.id
            )
            for cart_id in carts_id:
                cart = Cart.objects.get(id=cart_id)
                OrderProduct.objects.create(
                    order_id                = order.id,
                    product_id              = cart.product.id,
                    quantity                = cart.quantity,
                    order_product_status_id = 1
                )
            return JsonResponse({"message" : "ORDER_SUCCESS"}, status=201)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSONDecodeError'}, status=404)