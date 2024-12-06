from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), #главная
    path('catalog/', include('catalog.urls')), #каталог
    path('orders/', include('orders.urls', namespace='orders')),#заказы   #namespace ? оказалос для include нет поля nme, только namespace
    path('users/', include('users.urls')), #юзер
    path('reviews/', views.reviews, name='reviews'),  # Страница отзывов
    path('contacts/', views.contacts, name='contacts'),  # Маршрут для "Контакты"
    path('about/', views.about, name='about'),  # Маршрут для "О нас"
    path('cart/', include('cart.urls', namespace='cart')),  # Подключение маршрутов корзины
]


