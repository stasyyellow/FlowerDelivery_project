from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image')  # Отображаемые поля
    search_fields = ('name',)  # Поиск по названию
