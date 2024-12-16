from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from catalog.models import Product
from .models import Cart, CartItem

User = get_user_model()

class CartTestCase(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.product = Product.objects.create(name="Розы", price=1000)

    def test_cart_creation(self):
        """Тест: Создание корзины для пользователя"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('cart:cart_view'))
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(cart)

    def test_add_to_cart(self):
        """Тест: Добавление товара в корзину"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('cart:add_to_cart', args=[self.product.id]))
        cart = Cart.objects.get(user=self.user)
        cart_item = CartItem.objects.get(cart=cart, product=self.product)
        self.assertEqual(cart_item.quantity, 1)
        self.assertRedirects(response, reverse('catalog:product_list'))

    def test_decrease_quantity(self):
        """Тест: Уменьшение количества товара"""
        self.client.login(username='testuser', password='testpassword')
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        response = self.client.post(reverse('cart:decrease_quantity', args=[cart_item.id]))
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 1)

    def test_remove_from_cart(self):
        """Тест: Удаление товара из корзины"""
        self.client.login(username='testuser', password='testpassword')
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, product=self.product)
        response = self.client.post(reverse('cart:remove_from_cart', args=[cart_item.id]))
        self.assertFalse(CartItem.objects.filter(id=cart_item.id).exists())

    def test_cart_access_forbidden_for_anonymous(self):
        """Тест: Доступ к корзине неавторизованному пользователю"""
        response = self.client.get(reverse('cart:cart_view'))
        self.assertRedirects(response, '/users/login/?next=' + reverse('cart:cart_view'))

    def test_checkout(self):
        """Тест: Оформление заказа очищает корзину"""
        self.client.login(username='testuser', password='testpassword')
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        response = self.client.post(reverse('cart:checkout'))
        cart.refresh_from_db()
        self.assertEqual(cart.items.count(), 0)
        self.assertRedirects(response, reverse('catalog:product_list'))
