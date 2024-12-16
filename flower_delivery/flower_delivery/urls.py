from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('catalog/', include('catalog.urls', namespace='catalog')),  # Пространство имён
    path('cart/', include('cart.urls', namespace='cart')),
    path('users/', include('users.urls')),
    path('reviews/', views.reviews, name='reviews'),
    path('contacts/', views.contacts, name='contacts'),
    path('about/', views.about, name='about'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#namespace ? оказалос для include нет поля nme, только namespace