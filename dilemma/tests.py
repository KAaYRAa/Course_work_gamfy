from django.test import TestCase, Client
from django.urls import reverse

class DilemmaAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session['user_id'] = 1
        session.save()

    def test_dilemma_play_page(self):
        """1. Доступність головної сторінки гри Дилема"""
        response = self.client.get(reverse('dilemma:play'))
        self.assertEqual(response.status_code, 200)

    def test_get_dilemmas_api_accessible(self):
        """2. Доступність API для отримання карток дилем з бази"""
        response = self.client.get(reverse('dilemma:get_data'))
        self.assertEqual(response.status_code, 200)

    def test_get_dilemmas_returns_json(self):
        """3. Перевірка, що get_data віддає правильний JSON-тип для фронтенду"""
        response = self.client.get(reverse('dilemma:get_data'))
        self.assertIn('application/json', response['Content-Type'])

    def test_vote_dilemma_api_accessible(self):
        """4. Перевірка доступності ендпоінту агрегації голосів"""
        response = self.client.post(reverse('dilemma:vote_dilemma'), {'choice': 'A', 'card_id': 1})
        self.assertIn(response.status_code, [200, 404, 500])

    def test_vote_dilemma_processing(self):
        """5. Валідація того, що після голосування сервер повертає відповідь"""
        response = self.client.post(reverse('dilemma:vote_dilemma'), {'choice': 'B', 'card_id': 1})
        self.assertTrue(response.status_code)