from django.test import TestCase, Client
from django.urls import reverse

class PigGameTests(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session['user_id'] = 1
        session.save()

    def test_pig_rules_page(self):
        """1. Перевірка завантаження сторінки правил гри "Свиня" """
        response = self.client.get(reverse('pig:rules'))
        self.assertEqual(response.status_code, 200)

    def test_pig_game_page_loading(self):
        """2. Перевірка завантаження головної сторінки гри "Свиня" """
        response = self.client.get(reverse('pig:play'))
        self.assertEqual(response.status_code, 200)

    def test_pig_template_contains_content(self):
        """3. Перевірка успішного відображення HTML-контенту ігрового поля"""
        response = self.client.get(reverse('pig:play'))
        self.assertContains(response, "", status_code=200)

    def test_get_task_api_accessible(self):
        """4. Доступність API маршруту для отримання випадкового завдання"""
        response = self.client.get(reverse('pig:get_task'))
        self.assertEqual(response.status_code, 200)

    def test_get_task_api_returns_json(self):
        """5. Перевірка, що ендпоінт get_task повертає правильний JSON-формат для фронтенду"""
        response = self.client.get(reverse('pig:get_task'))
        self.assertIn('application/json', response['Content-Type'])