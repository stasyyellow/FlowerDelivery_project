from django.test import TestCase
from .models import Product


class ProductModelTest(TestCase):
    def test_create_product(self):
        # Создаем экземпляр модели Product
        product = Product.objects.create(name="Роза", price=100)

        # Проверяем, что имя продукта корректно
        self.assertEqual(product.name, "Роза")

        # Проверяем, что цена продукта корректна
        self.assertEqual(product.price, 100)
