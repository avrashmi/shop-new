from django.urls import path
from .views import ProductsView,ProductsDetailView

app_name='orders'

urlpatterns =[
    path('products/', ProductsView.as_view(), name='products'),
    path('product/<slug:slug>/', ProductsDetailView.as_view(), name='product_detail'),


]