from django.test import TestCase
from django.urls import reverse

class HomePageTests(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'flower_delivery/home.html')

# from django.test import TestCase
# from catalog.models import Product
#
# class ProductModelTest(TestCase):
#     def test_create_product(self):
#         product = Product.objects.create(name="Роза", price=100)
#         self.assertEqual(product.name, "Роза")
#         self.assertEqual(product.price, 100)
