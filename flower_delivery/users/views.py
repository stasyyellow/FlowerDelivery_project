from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm


# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались и вошли в систему!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации. Проверьте введенные данные.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


# Вход пользователя
def login_view(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        messages.success(request, 'Вы успешно вошли в систему!')
        return redirect('home')
    elif request.method == 'POST':
        messages.error(request, 'Ошибка входа. Проверьте правильность данных.')
    return render(request, 'users/login.html', {'form': form})


# Выход пользователя
def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('home')

