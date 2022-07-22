import json

from django.http     import JsonResponse
from django.views    import View

from carts.models    import Cart
from users.utils     import signin_decorator
from users.views     import LogInView
from products.models import Product
from users.models    import User


class CartView(View):
    @signin_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            quantity = data['quantity']
            product = Product.objects.get(id=data['product_id'])
            user = request.user
            
            Cart.objects.create(
                quantity = quantity,
                product = product,
                user = user
            )
            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'message':'JSONDecodeError'}, status=404)

    @signin_decorator
    def get(self, request):
        cart_products = [[cart.product.name, cart.quantity, cart.product.price] for cart in Cart.objects.filter(user=request.user)]
        return JsonResponse({"cart" : cart_products}, status=200)
    
    @signin_decorator
    def delete(self, request, cart_id):
        if Cart.objects.filter(user=request.user, id=cart_id).delete()[0]:
            return JsonResponse({"message":"SUCCESS"}, status=200)
        return JsonResponse({"message":"텅"}, status=400)
