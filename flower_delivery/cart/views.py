from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Product
from .models import Cart, CartItem
from django.contrib import messages
from orders.forms import OrderForm
from orders.models import Order, OrderItem

@login_required
def cart_view(request):
    """Просмотр содержимого корзины."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total = sum(item.get_total_price() for item in items)

    return render(request, 'cart/cart.html', {
        'items': items,
        'total': total,
    })

@login_required
def add_to_cart(request, product_id):
    """Добавление товара в корзину."""
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1
    cart_item.save()

    messages.success(request, f"Товар '{product.name}' был добавлен в корзину.")
    referer = request.META.get('HTTP_REFERER', '')
    if 'cart' in referer:
        return redirect('cart:cart_view')
    return redirect('catalog:product_list')

@login_required
def decrease_quantity(request, item_id):
    """Уменьшение количества товара в корзине."""
    cart_item = get_object_or_404(CartItem, id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.info(request, f"Количество товара '{cart_item.product.name}' уменьшено.")
    else:
        cart_item.delete()
        messages.info(request, f"Товар '{cart_item.product.name}' удален из корзины.")
    return redirect('cart:cart_view')

@login_required
def remove_from_cart(request, item_id):
    """Удаление одного товара из корзины."""
    cart_item = get_object_or_404(CartItem, id=item_id)
    messages.info(request, f"Товар '{cart_item.product.name}' был удален из корзины.")
    cart_item.delete()
    return redirect('cart:cart_view')

@login_required
def checkout(request):
    """Оформление заказа (с сайта)."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.source = 'web'  # Указываем источник заказа "сайт"
            order.save()

            for cart_item in items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

            cart.items.all().delete()

            messages.success(request, "Ваш заказ успешно оформлен!")
            return redirect('catalog:product_list')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = OrderForm()

    return render(request, 'cart/checkout.html', {
        'items': items,
        'form': form
    })

