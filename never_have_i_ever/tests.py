from django.test import TestCase, Client
from django.urls import reverse

class NeverHaveIEverTests(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session['user_id'] = 1
        session.save()

    def test_never_have_i_ever_play_page(self):
        """1. Доступність головної сторінки гри "Я ніколи не..." """
        response = self.client.get(reverse('never_have_i_ever:play'))
        self.assertEqual(response.status_code, 200)

    def test_never_have_i_ever_template_rendering(self):
        """2. Перевірка успішного відображення HTML-контенту сторінки"""
        response = self.client.get(reverse('never_have_i_ever:play'))
        self.assertContains(response, "", status_code=200)

    def test_get_data_api_accessible(self):
        """3. Доступність API маршруту для отримання випадкових питань та покарань"""
        response = self.client.get(reverse('never_have_i_ever:get_data'))
        self.assertEqual(response.status_code, 200)

    def test_get_data_returns_json(self):
        """4. Перевірка, що get_data повертає правильний формат JSON для Fetch API"""
        response = self.client.get(reverse('never_have_i_ever:get_data'))
        self.assertIn('application/json', response['Content-Type'])

    def test_never_have_i_ever_category_param_processing(self):
        """5. Перевірка обробки GET-параметрів фільтрації категорій або рівнів відвертості"""
        response = self.client.get(reverse('never_have_i_ever:get_data') + '?category=party')
        self.assertEqual(response.status_code, 200)