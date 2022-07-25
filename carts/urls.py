from django.urls import path

from carts.views import CartToOrderView, CartView

urlpatterns = [
    path('', CartView.as_view()),
    path('/neworder', CartToOrderView.as_view())
]