from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='cart_view'),  # Просмотр корзины
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Добавление товара
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # Удаление товара
    path('decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),  # Уменьшение количества
    path('checkout/', views.checkout, name='checkout'),  # Оформление заказа
]

