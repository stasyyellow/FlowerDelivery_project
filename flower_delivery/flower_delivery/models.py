from django.db import models
from django.conf import settings

class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    text = models.TextField(verbose_name="Текст отзыва")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return f"Отзыв от {self.user.username}"

class Slide(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название слайда")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to='slides/', verbose_name="Изображение")
    is_trend = models.BooleanField(default=False, verbose_name="Тренд сезона")

    def __str__(self):
        return self.title
