from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OrderForm
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem


@login_required
def create_order(request):
    """Создание заказа с товарами из корзины."""
    cart = Cart.objects.filter(user=request.user).first()

    if not cart or not cart.items.exists():
        messages.error(request, "Ваша корзина пуста.")
        return redirect('cart:cart_view')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            # Перенести товары из корзины в заказ
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
            # Очистить корзину
            cart.items.all().delete()

            messages.success(request, 'Ваш заказ успешно создан!')
            return redirect('home')
    else:
        form = OrderForm()

    return render(request, 'orders/create_order.html', {'form': form})

