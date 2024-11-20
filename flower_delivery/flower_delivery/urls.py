from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Админка
    path('', views.home, name='home'),  # Главная страница
    path('users/', include('users.urls')),  # Маршруты приложения users
    path('catalog/', include('catalog.urls')),  # Маршруты приложения catalog
    path('orders/', include('orders.urls')),  # Маршруты приложения orders
]
