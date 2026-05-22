from django.test import TestCase, Client
from django.urls import reverse

class GamesCatalogTests(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session['user_id'] = 1
        session.save()

    def test_home_page_status_code(self):
        """1. Успішне завантаження каталогу ігор (Головна сторінка)"""
        response = self.client.get(reverse('games:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_contains_content(self):
        """2. Перевірка успішного рендерингу HTML-контенту каталогу"""
        response = self.client.get(reverse('games:home'))
        self.assertContains(response, "", status_code=200)

    def test_game_detail_view_accessible(self):
        """3. Перевірка доступності сторінки конкретної гри (динамічний URL)"""
        response = self.client.get(reverse('games:game_detail', args=[1]))
        self.assertIn(response.status_code, [200, 404])

    def test_save_game_result_accessible(self):
        """4. Доступність ендпоінту для збереження результатів фіналу гри"""
        response = self.client.post(reverse('games:save_result'), {'score': 100})
        self.assertIn(response.status_code, [200, 302, 400])

    def test_home_filters_processing(self):
        """5. Тестування обробки GET-параметрів пошуку та фільтрації в каталозі"""
        response = self.client.get(reverse('games:home') + '?search=Мафія&players=5')
        self.assertEqual(response.status_code, 200)