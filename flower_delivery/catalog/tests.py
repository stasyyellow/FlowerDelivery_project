from django.test import TestCase
from django.urls import reverse
from .models import Product


class ProductModelTest(TestCase):
    def test_create_product(self):
        product = Product.objects.create(name="Роза", price=100)
        self.assertEqual(product.name, "Роза")
        self.assertEqual(product.price, 100)


class ProductListViewTests(TestCase):
    def setUp(self):
        Product.objects.create(name="Роза", price=100)
        Product.objects.create(name="Лилия", price=200)

    def test_product_list_view(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Роза")
        self.assertContains(response, "Лилия")
        self.assertTemplateUsed(response, 'catalog/product_list.html')
