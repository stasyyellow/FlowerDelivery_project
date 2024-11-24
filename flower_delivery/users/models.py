from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Номер телефона"
    )

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Уникальное значение для related_name
        blank=True,
        verbose_name="Группы"
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Уникальное значение для related_name
        blank=True,
        verbose_name="Разрешения"
    )

    def __str__(self):
        return f"{self.username} ({self.phone_number or 'Телефон не указан'})"


