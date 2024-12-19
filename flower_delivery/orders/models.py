from django.conf import settings
from django.db import models
from catalog.models import Product

class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    delivery_address = models.CharField(
        max_length=255,
        verbose_name="Адрес доставки"
    )
    add_card = models.BooleanField(
        default=False,
        verbose_name="Добавить открытку?"
    )
    card_text = models.TextField(
        blank=True,
        null=True,
        verbose_name="Текст открытки"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Ожидает'),
            ('completed', 'Завершен'),
            ('cancelled', 'Отменен'),
        ],
        default='pending',
        verbose_name="Статус"
    )
    source = models.CharField(
        max_length=10,
        choices=[('web', 'Сайт'), ('telegram', 'Телеграм')],
        default='web',
        verbose_name="Источник заказа"
    )

    def __str__(self):
        return f"Заказ {self.id} от {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Заказ"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Количество"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за единицу"
    )

    def get_total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
