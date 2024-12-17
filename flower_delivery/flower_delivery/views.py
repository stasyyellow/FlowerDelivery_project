from django.shortcuts import render, redirect
from catalog.models import Product
from .models import Review, Slide

from .models import Slide

def home(request):
    """
    Главная страница.
    Вывод случайных товаров и слайдов.
    """
    # Случайные товары
    products = Product.objects.order_by('?')[:3]

    # Все слайды (без фильтра по is_trend)
    trend_slides = Slide.objects.all().order_by('id')[:5]

    context = {
        'products': products,
        'trend_slides': trend_slides,
    }

    # Рендеринг шаблона с передачей контекста
    return render(request, 'flower_delivery/home.html', context)


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
