from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Количество дополнительных строк в админке

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'delivery_address', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'delivery_address')
    inlines = [OrderItemInline]  # Для отображения элементов заказа в форме заказа

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')
    search_fields = ('product__name',)

# from django.contrib import admin
# from .models import Order
#
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'product', 'quantity', 'status', 'created_at')
#     list_filter = ('status', 'created_at')
#     search_fields = ('user__username', 'product__name')