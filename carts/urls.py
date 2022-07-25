from django.urls import path

from carts.views import CartView, CartToOrderView

urlpatterns = [
    path('', CartView.as_view()),
    path('/<int:cart_id>', CartView.as_view()),
    path('/neworder', CartToOrderView.as_view())
]