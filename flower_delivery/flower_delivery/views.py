from django.shortcuts import render
from catalog.models import Product


def home(request):
    products = Product.objects.order_by('?')[:3]
    return render(request, 'flower_delivery/home.html', {'products': products})


