from django.shortcuts import render, redirect
from catalog.models import Product #?
from .models import Review

def home(request):
    products = Product.objects.order_by('?')[:3]
    return render(request, 'flower_delivery/home.html', {'products': products})


# Отображение страницы отзывов
def reviews(request):
    if request.method == 'POST' and request.user.is_authenticated:
        text = request.POST.get('review')
        if text:
            Review.objects.create(user=request.user, text=text)
            return redirect('reviews')
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'flower_delivery/reviews.html', {'reviews': reviews})

def contacts(request):
    return render(request, 'flower_delivery/contacts.html')

def about(request):
    return render(request, 'flower_delivery/about.html')
