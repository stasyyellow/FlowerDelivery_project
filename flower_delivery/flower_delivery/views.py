from django.shortcuts import render, redirect
from catalog.models import Product
from .models import Review, Slide

def home(request):
    """
    Главная страница.
    Вывод случайных товаров, сезонных и трендовых слайдов.
    """
    # Случайные товары
    products = Product.objects.order_by('?')[:3]

    # Сезонные и трендовые слайды
    seasonal_slides = Slide.objects.filter(is_trend=False).order_by('id')[:5]
    trend_slides = Slide.objects.filter(is_trend=True).order_by('id')[:5]

    # Контекст для передачи данных
    context = {
        'products': products,
        'seasonal_slides': seasonal_slides,
        'trend_slides': trend_slides,
    }

    # Рендеринг шаблона с передачей контекста
    return render(request, 'flower_delivery/home.html', context) #context

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
