from django.urls import path
from django.views import View

from carts.views import CartView

urlpatterns = [
    path('', CartView.as_view())
]