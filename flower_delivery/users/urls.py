from django.urls import path
from . import views

app_name = 'users'  # Это позволяет использовать пространство имён 'users'

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),  # Маршрут для выхода
    path('login/', views.login_view, name='login'),    # Маршрут для входа
    path('register/', views.register, name='register')  # Маршрут для регистрации
]
