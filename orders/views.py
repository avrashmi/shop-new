from django.shortcuts import render
from django.views.generic import ListView,DetailView
from products.models import Products
# Create your views here.

class ProductsView(ListView):
    model = Products
    template_name ='orders/product_list.html'

class ProductsDetailView(DetailView):
    model = Products
    template_name ='orders/product_detail.html'
    