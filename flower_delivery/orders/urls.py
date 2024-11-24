from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Маршрут для создания заказа
    path('create/', views.create_order, name='create_order'),
    # Маршрут для создания заказа с предвыбранным товаром
    path('create/<int:product_id>/', views.create_order, name='create_order_with_product'),
]
