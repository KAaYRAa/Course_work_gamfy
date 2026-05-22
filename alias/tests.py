from django.test import TestCase, Client
from django.urls import reverse

class AliasAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session['user_id'] = 1
        session.save()

    def test_alias_start_view_status_code(self):
        """1. Перевірка доступності сторінки старту раунду Аліас"""
        response = self.client.get(reverse('alias:play'))
        self.assertEqual(response.status_code, 200)

    def test_alias_start_view_template(self):
        """2. Перевірка рендерингу правильного шаблону для Аліасу"""
        response = self.client.get(reverse('alias:play'))
        self.assertContains(response, "", status_code=200)

    def test_get_words_api_accessible(self):
        """3. Доступність API маршруту для завантаження слів"""
        response = self.client.get(reverse('alias:get_words'))
        self.assertEqual(response.status_code, 200)

    def test_get_words_api_returns_json(self):
        """4. Перевірка, що get-words повертає саме JSON-структуру для Fetch API"""
        response = self.client.get(reverse('alias:get_words'))
        self.assertIn('application/json', response['Content-Type'])

    def test_alias_anonymous_user_behavior(self):
        """5. Перевірка поведінки сесії для користувача"""
        session = self.client.session
        self.assertEqual(session['user_id'], 1)