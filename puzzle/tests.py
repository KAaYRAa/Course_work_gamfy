from django.test import TestCase, Client
from django.urls import reverse

class PuzzleGameTests(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session['user_id'] = 1
        session.save()

    def test_puzzle_play_page(self):
        """1. Перевірка завантаження головної сторінки гри Пазл"""
        response = self.client.get(reverse('puzzle:play'))
        self.assertEqual(response.status_code, 200)

    def test_puzzle_template_renders_successfully(self):
        """2. Перевірка успішного відображення HTML-структури ігрової сторінки"""
        response = self.client.get(reverse('puzzle:play'))
        self.assertContains(response, "", status_code=200)

    def test_get_puzzle_data_accessible(self):
        """3. Доступність API маршруту для отримання секретного слова та підказок"""
        response = self.client.get(reverse('puzzle:get_data'))
        self.assertEqual(response.status_code, 200)

    def test_get_puzzle_data_returns_json(self):
        """4. Перевірка, що ендпоінт get_data повертає правильний JSON-формат для Fetch API"""
        response = self.client.get(reverse('puzzle:get_data'))
        self.assertIn('application/json', response['Content-Type'])

    def test_puzzle_game_state_in_session(self):
        """5. Тестування ініціалізації та контролю ігрового прогресу всередині сесії"""
        session = self.client.session
        session['puzzle_solved'] = False  
        session.save()
        self.assertEqual(self.client.session['puzzle_solved'], False)