from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Количество дополнительных строк в админке

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'delivery_address', 'add_card', 'card_text', 'status', 'source', 'created_at')
    list_filter = ('status', 'add_card', 'source', 'created_at')
    search_fields = ('user__username', 'delivery_address', 'card_text', 'source')
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')
    search_fields = ('product__name',)

