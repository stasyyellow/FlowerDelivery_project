from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserTests(TestCase):
    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        })
        self.assertEqual(response.status_code, 302)  # Редирект после регистрации
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login_user(self):
        User.objects.create_user(username='testuser', password='strongpassword123')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'strongpassword123',
        })
        self.assertEqual(response.status_code, 302)  # Редирект после входа
