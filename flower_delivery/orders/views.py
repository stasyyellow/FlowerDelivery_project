from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OrderForm
from cart.models import Cart, CartItem
from .models import Order, OrderItem
import requests
from config import BOT_TOKEN, TG_ID


def send_order_to_telegram(order):
    """Отправка данных о заказе в Telegram админу."""
    token = BOT_TOKEN
    chat_id = TG_ID
    message = (f"📦 Новый заказ!\n\n"
               f"👤 Пользователь: {order.user.username}\n"
               f"📍 Адрес доставки: {order.delivery_address}\n"
               f"📄 Открытка: {'Да' if order.add_card else 'Нет'}\n"
               f"📝 Текст открытки: {order.card_text or 'Без открытки'}\n"
               f"🕒 Дата заказа: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
               f"🛒 Состав заказа:\n")
    for item in order.items.all():
        message += f"   - {item.product.name} x {item.quantity} (Цена: {item.price} руб.)\n"

    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, data=data)

    if response.status_code != 200:
        print(f"Ошибка отправки заказа в Telegram: {response.text}")


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
            try:
                # Создаем объект заказа
                order = form.save(commit=False)
                order.user = request.user
                order.save()

                # Переносим товары из корзины в заказ
                for cart_item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price
                    )

                # Очищаем корзину
                cart.items.all().delete()

                # Отправляем заказ админу через Telegram
                try:
                    send_order_to_telegram(order)
                except Exception as e:
                    print(f"Ошибка отправки в Telegram: {e}")

                messages.success(request, 'Ваш заказ успешно создан! Мы скоро с вами свяжемся.')
                return redirect('home')

            except Exception as e:
                print(f"Ошибка при создании заказа: {e}")
                messages.error(request, "Произошла ошибка при оформлении заказа. Попробуйте снова.")
                return redirect('cart:cart_view')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = OrderForm()

    return render(request, 'orders/create_order.html', {'form': form})
