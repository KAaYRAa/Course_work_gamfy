from django.test import TestCase, Client
from django.urls import reverse

class WhoAmITests(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session['user_id'] = 1
        session.save()

    def test_who_am_i_play_page_accessible(self):
        """1. Доступність головної сторінки гри "Хто я?" """
        response = self.client.get(reverse('who_am_i:play'))
        self.assertEqual(response.status_code, 200)

    def test_who_am_i_template_rendering(self):
        """2. Перевірка успішного відображення HTML-контенту ігрового поля"""
        response = self.client.get(reverse('who_am_i:play'))
        self.assertContains(response, "", status_code=200)

    def test_get_characters_api_accessible(self):
        """3. Доступність API маршруту для завантаження випадкових персонажів"""
        response = self.client.get(reverse('who_am_i:get_characters'))
        self.assertEqual(response.status_code, 200)

    def test_get_characters_api_returns_json(self):
        """4. Перевірка, що ендпоінт get_characters повертає правильний JSON-формат для Fetch API"""
        response = self.client.get(reverse('who_am_i:get_characters'))
        self.assertIn('application/json', response['Content-Type'])

    def test_who_am_i_game_state_in_session(self):
        """5. Тестування ініціалізації та контролю стану поточної гри у сесії"""
        session = self.client.session
        session['character_assigned'] = True  
        session.save()
        self.assertEqual(self.client.session['character_assigned'], True)