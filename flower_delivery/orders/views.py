from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OrderForm


@login_required
def create_order(request, product_id=None):
    """
    Представление для создания заказа.
    - Только авторизованные пользователи могут создавать заказ.
    - Если передан product_id, форма заполняется этим товаром.
    """
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user  # Устанавливаем текущего пользователя как автора заказа
            order.save()
            messages.success(request, 'Ваш заказ успешно создан!')
            return redirect('product_list')  # Перенаправляем пользователя в каталог
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        # Если передан product_id, заполняем форму предварительными данными
        initial_data = {'product': product_id} if product_id else {}
        form = OrderForm(initial=initial_data)

    return render(request, 'orders/create_order.html', {'form': form})
