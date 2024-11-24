from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('catalog/', include('catalog.urls')),
    path('orders/', include('orders.urls', namespace='orders')), #namespace ? оказалос для include нет поля nme, только namespace
    path('users/', include('users.urls')),
]
