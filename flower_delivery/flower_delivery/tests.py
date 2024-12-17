from django.test import TestCase
from django.urls import reverse
from .models import Slide
from django.core.files.uploadedfile import SimpleUploadedFile


class FlowerDeliverySimpleTests(TestCase):
    """Базовые тесты для приложения flower_delivery."""

    def setUp(self):
        # Создаем моковое изображение
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")

        # Создаем трендовый слайд с изображением
        Slide.objects.create(
            title="Trend Slide",
            description="Trending flowers",
            is_trend=True,
            image=image
        )

    def test_home_page_with_trend_slide(self):
        """Тест главной страницы: наличие трендового слайда."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Trending flowers")  # Проверяем описание
        self.assertContains(response, "Trend Slide")  # Проверяем название

    def test_reviews_page(self):
        """Тест страницы отзывов."""
        response = self.client.get(reverse('reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Отзывы")  # Проверяем заголовок страницы

    def test_contacts_page(self):
        """Тест страницы контактов."""
        response = self.client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Контакты")

    def test_about_page(self):
        """Тест страницы 'О нас'."""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "О нас")
