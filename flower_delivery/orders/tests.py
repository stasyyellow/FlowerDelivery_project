from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from orders.models import Order, OrderItem
from catalog.models import Product
from cart.models import Cart, CartItem
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


class OrderTestCase(TestCase):
    def setUp(self):
        # Создаём пользователя
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        # Создаём моковое изображение
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b',
            content_type='image/jpeg'
        )

        # Создаём товар с изображением
        self.product = Product.objects.create(
            name='Роза',
            price=100.00,
            description='Свежие розы',
            image=image
        )

        # Создаём корзину для пользователя
        self.cart = Cart.objects.create(user=self.user)

        # URL для создания заказа
        self.create_order_url = reverse('orders:create_order')

    def test_create_order_with_items(self):
        """Тест: создание заказа с товарами из корзины."""
        # Добавляем товар в корзину
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

        # Отправляем POST-запрос на создание заказа
        response = self.client.post(self.create_order_url, data={
            'delivery_address': 'ул. Тестовая, д. 1',
            'comment': 'Тестовый заказ',
        })

        # Проверяем редирект на главную страницу
        self.assertRedirects(response, reverse('home'))

        # Проверяем, что заказ был создан
        self.assertTrue(Order.objects.filter(user=self.user).exists(), "Заказ не был создан")

        # Проверяем, что корзина очищена
        self.assertFalse(CartItem.objects.filter(cart=self.cart).exists(), "Корзина не была очищена")

    def test_create_order_with_empty_cart(self):
        """Тест: попытка создания заказа с пустой корзиной."""
        # Отправляем POST-запрос при пустой корзине
        response = self.client.post(self.create_order_url)

        # Проверяем редирект на страницу корзины
        self.assertRedirects(response, reverse('cart:cart_view'))

        # Проверяем, что заказ не был создан
        self.assertFalse(Order.objects.filter(user=self.user).exists(), "Заказ был создан при пустой корзине")

        # Проверяем сообщение об ошибке
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Ваша корзина пуста.")
