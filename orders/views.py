import json

from django.views import View
from core.models import TimeStampModel
from orders.models import Order, OrderProduct
from users.utils import signin_decorator

"""
post + delete(cart) - 장바구니에서 order로 추가하는 동시에, cart에서 삭제
get - 주문 상세 페이지
delete - order 상세 페이지에서 주문 취소
"""

@signin_decorator
class OrderView(TimeStampModel):
    def post(self, request):
        try:
            data    = json.loads(request.body)
            cart_id = data['cart_id']
            
            Order.objects.create(
                order_status_id = 1,
                user_id         = request.user.id
            )
            OrderProduct.objects.create(
                order_id = ,
                product_id = ,
                quantity = ,
                order_products_status = 1
            )

        except:
            return