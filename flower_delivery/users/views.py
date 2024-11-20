from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем нового пользователя
            login(request, user)  # Входим в систему после регистрации
            messages.success(request, 'Вы успешно зарегистрировались и вошли в систему!')  # Успешное сообщение
            return redirect('home')  # Перенаправляем на главную страницу
        else:
            messages.error(request, 'Ошибка регистрации. Проверьте введенные данные.')  # Ошибка регистрации
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# Вход пользователя
def login_view(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        login(request, form.get_user())  # Вход в систему
        messages.success(request, 'Вы успешно вошли в систему!')  # Успешное сообщение
        return redirect('home')
    elif request.method == 'POST':
        messages.error(request, 'Ошибка входа. Проверьте правильность данных.')  # Ошибка входа
    return render(request, 'users/login.html', {'form': form})

# Выход пользователя
def logout_view(request):
    logout(request)  # Выход из системы
    messages.info(request, 'Вы вышли из системы.')  # Сообщение об успешном выходе
    return redirect('home')  # Перенаправляем на главную






# from django.shortcuts import render, redirect
# from django.contrib.auth import login
# from .forms import CustomUserCreationForm
#
# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'users/register.html', {'form': form})