from django.test import TestCase
from django.urls import reverse
from .models import Product

class ProductListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Создаем тестовые данные для продуктов."""
        Product.objects.create(
            name="Розы",
            price=1200.00,
            description="Букет роз",
            image=None
        )
        Product.objects.create(
            name="Тюльпаны",
            price=800.00,
            description="Букет тюльпанов",
            image=None
        )

    def test_product_list_page_status_code(self):
        """Проверка доступности страницы списка товаров."""
        response = self.client.get(reverse('catalog:product_list'))
        self.assertEqual(response.status_code, 200)

    def test_product_list_template_used(self):
        """Проверка использования корректного шаблона."""
        response = self.client.get(reverse('catalog:product_list'))
        self.assertTemplateUsed(response, 'catalog/product_list.html')

    def test_product_list_context(self):
        """Проверка, что в контексте передаются товары из базы данных."""
        response = self.client.get(reverse('catalog:product_list'))
        self.assertTrue('products' in response.context)

        products = response.context['products']
        self.assertEqual(len(products), 2)  # Проверка, что два продукта переданы

        # Проверяем конкретные названия товаров
        product_names = [product.name for product in products]
        self.assertIn("Розы", product_names)
        self.assertIn("Тюльпаны", product_names)
