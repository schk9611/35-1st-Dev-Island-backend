from django.urls import path

from .views import ProductListView

urlpatterns = [
    path('/<str:category>', ProductListView.as_view()),
]