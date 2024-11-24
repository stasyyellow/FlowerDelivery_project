from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserTests(TestCase):
    def test_register_user(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'phone_number': '+1234567890',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(User.objects.filter(phone_number='+1234567890').exists())

    def test_register_with_invalid_phone(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'phone_number': 'invalidphone',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        })
        self.assertEqual(response.status_code, 200)  # Ошибка остаётся на форме
        self.assertFalse(User.objects.filter(username='testuser').exists())
