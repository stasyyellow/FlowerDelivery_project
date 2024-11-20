from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")  # Название товара
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")  # Цена товара
    description = models.TextField(blank=True, null=True, verbose_name="Описание")  # Описание (необязательно)
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Изображение товара")  # Изображение товара

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name

# from django.db import models
# class Product(models.Model):
#     name = models.CharField(max_length=100)  # Название товара
#     price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена товара
#     description = models.TextField(blank=True, null=True)  # Описание (необязательно)
#     image = models.ImageField(upload_to='products/', blank=True, null=True)  # Изображение товара
#
#     def __str__(self):
#         return self.name




