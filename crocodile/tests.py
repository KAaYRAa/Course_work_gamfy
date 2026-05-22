from django.test import TestCase, Client
from django.urls import reverse

class CrocodileAppTests(TestCase):
    def setUp(self):
        self.client = Client()

        session = self.client.session
        session['user_id'] = 1
        session.save()

    def test_crocodile_start_page(self):
        """1. Доступність головного меню гри Крокодил"""
        response = self.client.get(reverse('crocodile:play'))
        self.assertEqual(response.status_code, 200)

    def test_crocodile_template_used(self):
        """2. Перевірка, що сторінка гри віддає контент без помилок сервера"""
        response = self.client.get(reverse('crocodile:play'))
        self.assertContains(response, "", status_code=200)

    def test_get_words_api_accessible(self):
        """3. Доступність API маршруту для отримання ігрових слів"""
        response = self.client.get(reverse('crocodile:get_words'))
        self.assertEqual(response.status_code, 200)

    def test_get_words_returns_json(self):
        """4. Перевірка, що get_words повертає правильний формат JSON для фронтенду"""
        response = self.client.get(reverse('crocodile:get_words'))
        self.assertIn('application/json', response['Content-Type'])

    def test_crocodile_difficulty_param_processing(self):
        """5. Перевірка обробки GET-параметрів фільтрації (наприклад, рівня складності)"""
        response = self.client.get(reverse('crocodile:get_words') + '?difficulty=easy')
        self.assertEqual(response.status_code, 200)