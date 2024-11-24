from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from catalog.models import Product
from .models import Order

User = get_user_model()

class OrderTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.product = Product.objects.create(name='Тестовый продукт', price=100)

    def test_create_order(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('orders:create_order'), {
            'product': self.product.id,
            'quantity': 2,
            'delivery_address': 'Тестовый адрес',
            'comment': 'Тестовый комментарий',
        })
        self.assertEqual(response.status_code, 302)  # Редирект после успешного создания
        self.assertTrue(Order.objects.filter(user=self.user, product=self.product).exists())
