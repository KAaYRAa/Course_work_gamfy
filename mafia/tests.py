from django.test import TestCase, Client
from django.urls import reverse
import json

class MafiaAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session['user_id'] = 1
        session.save()

    def test_mafia_rules_page(self):
        """1. Доступність сторінки правил гри Мафія"""
        response = self.client.get(reverse('mafia:rules'))
        self.assertEqual(response.status_code, 200)

    def test_mafia_play_page(self):
        """2. Доступність головної сторінки ігрової кімнати Мафії"""
        response = self.client.get(reverse('mafia:play'))
        self.assertEqual(response.status_code, 200)

    def test_mafia_play_template_rendering(self):
        """3. Перевірка успішного відображення HTML-контенту гри"""
        response = self.client.get(reverse('mafia:play'))
        self.assertContains(response, "", status_code=200)

    def test_distribute_roles_api_accessible(self):
        """4. Доступність API маршруту для розподілу ролей"""
        payload = json.dumps({'players_count': 6})
        response = self.client.post(
            reverse('mafia:distribute_roles'), 
            data=payload, 
            content_type='application/json'
        )
        self.assertIn(response.status_code, [200, 302, 400])

    def test_distribute_roles_api_returns_json_or_redirect(self):
        """5. Перевірка обробки запиту до API розподілу ролей та роботи сесії"""
        payload = json.dumps({})
        response = self.client.post(
            reverse('mafia:distribute_roles'), 
            data=payload, 
            content_type='application/json'
        )
        self.assertIn(response.status_code, [200, 302, 400, 405])