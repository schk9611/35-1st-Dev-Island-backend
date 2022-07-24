import json

from django.http     import JsonResponse
from django.views    import View

from carts.models    import Cart
from users.utils     import signin_decorator
from products.models import Product

class CartView(View):
    @signin_decorator
    def post(self, request):
        try:
            data     = json.loads(request.body)
            quantity = data['quantity']
            product  = Product.objects.get(id=data['product_id'])
            user     = request.user
            
            Cart.objects.create(
                quantity = quantity,
                product  = product,
                user     = user
            )
            return JsonResponse({"message" : "PUT_IN_CART_SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'message':'JSONDecodeError'}, status=404)

    @signin_decorator
    def get(self, request):
        cart_products = [{
            'product_name': cart.product.name,
            'quantity'    : cart.quantity,
            'price'       : cart.product.price,
            'images'      : [image.image_url for image in cart.product.productimage_set.all()]}
            for cart in Cart.objects.filter(user=request.user)]
        return JsonResponse({"message" : "SUCCESS", "cart" : cart_products}, status=200)
    
    @signin_decorator
    def delete(self, request):
        try:
            data = json.loads(request.body)
            for cart_id in data['carts_id']:
                Cart.objects.filter(user=request.user, id=cart_id).delete()
            return JsonResponse({"message":"DELETE_SUCCESS"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'message':'JSONDecodeError'}, status=404)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        
    @signin_decorator
    def patch(self, request, cart_id):
        try: 
            data         = json.loads(request.body)
            cart_product = Cart.objects.get(user=request.user, id=cart_id)
            
            if cart_product.product.stock < data['stock']:
                return JsonResponse({"message" : "OUT_OF_STOCK"}, status=400)
            
            cart_product.quantity = data['stock']
            cart_product.save()
            return JsonResponse({"message" : "UPDATE_SUCCESS"})

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

        except Cart.DoesNotExist:
            return JsonResponse({'message':'JSONDecodeError'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'message':'JSONDecodeError'}, status=404)