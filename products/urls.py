from django.urls    import path

from products.views import DetailView
from products.models import Product

urlpatterns = [
    path('/detail/<product_id>', DetailView.as_view()),
]