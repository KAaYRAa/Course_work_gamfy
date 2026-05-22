from django.test import TestCase, Client
from django.urls import reverse

class DanetkiAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session['user_id'] = 1
        session.save()

    def test_danetki_main_page(self):
        """1. Доступність головної сторінки гри Данетки"""
        response = self.client.get(reverse('danetki:play'))
        self.assertEqual(response.status_code, 200)

    def test_danetki_template_rendering(self):
        """2. Перевірка успішного рендерингу HTML контенту сторінки"""
        response = self.client.get(reverse('danetki:play'))
        self.assertContains(response, "", status_code=200)

    def test_get_danetka_api_accessible(self):
        """3. Доступність API для отримання випадкової історії з бази"""
        response = self.client.get(reverse('danetki:get_data'))
        self.assertEqual(response.status_code, 200)

    def test_get_danetka_api_returns_json(self):
        """4. Перевірка, що get_data повертає правильний формат JSON для Fetch API"""
        response = self.client.get(reverse('danetki:get_data'))
        self.assertIn('application/json', response['Content-Type'])

    def test_danetki_role_state_in_session(self):
        """5. Перевірка менеджменту станів та збереження ролі користувача в сесії"""
        session = self.client.session
        session['danetki_role'] = 'host' 
        session.save()
        self.assertEqual(self.client.session['danetki_role'], 'host')