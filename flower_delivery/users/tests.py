from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UsersTestCase(TestCase):
    def setUp(self):
        self.register_url = reverse('users:register')
        self.user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'phone_number': '1234567890',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!'
        }

    def test_register_user_valid_data(self):
        """Тест: успешная регистрация пользователя."""
        response = self.client.post(self.register_url, self.user_data)

        # Проверка редиректа
        self.assertRedirects(response, reverse('home'))

        # Проверка создания пользователя
        self.assertTrue(User.objects.filter(username=self.user_data['username']).exists())

    def test_register_user_invalid_data(self):
        """Тест: ошибка при регистрации с неверными данными."""
        invalid_data = self.user_data.copy()
        invalid_data['username'] = ''  # Пустое имя пользователя
        invalid_data['password2'] = 'wrongpassword'  # Несовпадающие пароли

        response = self.client.post(self.register_url, invalid_data)

        # Проверка статуса страницы и наличия формы
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

        # Проверка ошибок формы
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('username', form.errors)
        self.assertIn('password2', form.errors)

    def test_register_user_duplicate_username(self):
        """Тест: ошибка при регистрации с уже существующим именем пользователя."""
        User.objects.create_user(username='newuser', password='TestPassword123!')
        response = self.client.post(self.register_url, self.user_data)

        # Проверка, что форма вернула ошибку
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('username', form.errors)

    def test_register_user_missing_field(self):
        """Тест: ошибка при регистрации с отсутствующим полем."""
        incomplete_data = self.user_data.copy()
        incomplete_data.pop('password1')  # Убираем обязательное поле

        response = self.client.post(self.register_url, incomplete_data)

        # Проверка, что форма вернула ошибку
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('password1', form.errors)

    def test_register_user_shows_error_messages(self):
        """Тест: отображение ошибок формы на странице."""
        invalid_data = self.user_data.copy()
        invalid_data['username'] = ''  # Пустое имя пользователя

        response = self.client.post(self.register_url, invalid_data)

        # Проверка наличия сообщения об ошибке
        self.assertContains(response, 'Обязательное поле.')
