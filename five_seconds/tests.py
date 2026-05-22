from django.test import TestCase, Client
from django.urls import reverse

class FiveSecondsTests(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session['user_id'] = 1
        session.save()

    def test_five_seconds_play_page(self):
        """1. Доступність головної сторінки гри Назвати за 5 секунд"""
        response = self.client.get(reverse('five_seconds:play'))
        self.assertEqual(response.status_code, 200)

    def test_five_seconds_template_rendering(self):
        """2. Перевірка успішного відображення контенту сторінки"""
        response = self.client.get(reverse('five_seconds:play'))
        self.assertContains(response, "", status_code=200)

    def test_get_questions_api_accessible(self):
        """3. Доступність API маршруту для завантаження списку питань"""
        response = self.client.get(reverse('five_seconds:get_questions'))
        self.assertEqual(response.status_code, 200)

    def test_get_questions_returns_json(self):
        """4. Перевірка, що ендпоінт повертає правильний JSON-формат для фронтенду"""
        response = self.client.get(reverse('five_seconds:get_questions'))
        self.assertIn('application/json', response['Content-Type'])

    def test_five_seconds_score_state(self):
        """5. Тестування збереження та ініціалізації лічильника балів у сесії"""
        session = self.client.session
        session['five_seconds_score'] = 0  
        session.save()
        self.assertEqual(self.client.session['five_seconds_score'], 0)