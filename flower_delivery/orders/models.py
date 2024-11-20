from flower_delivery.catalog.models import Product #абсолютный путь
from django.conf import settings
from django.db import models

class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )  # Связь с пользователем
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )  # Связь с товаром
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Количество"
    )  # Количество товара
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )  # Дата создания заказа
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Ожидает'),
            ('completed', 'Завершен'),
            ('cancelled', 'Отменен'),
        ],
        default='pending',
        verbose_name="Статус"
    )  # Статус заказа

    def __str__(self):
        return f"Заказ {self.id} от {self.user.username}"



# from django.db import models
# from django.conf import settings
#
# class Order(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     created_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=20, choices=[
#         ('pending', 'Ожидает'),
#         ('completed', 'Завершен'),
#         ('cancelled', 'Отменен')
#     ], default='pending')
#
#     def __str__(self):
#         return f"Заказ {self.id} от {self.user.username}"
