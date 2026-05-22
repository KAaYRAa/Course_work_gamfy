from django.test import TestCase, Client
from django.urls import reverse

class UsersAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session['user_id'] = 1
        session.save()

    def test_login_view_accessible(self):
        """1. Перевірка доступності сторінки входу (Login)"""
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_accessible(self):
        """2. Перевірка доступності сторінки реєстрації (Register)"""
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)

    def test_profile_view_accessible_with_session(self):
        """3. Перевірка доступності особистого кабінету при наявній сесії"""
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)

    def test_user_history_view_accessible(self):
        """4. Перевірка доступності сторінки історії зіграних ігор"""
        response = self.client.get(reverse('users:user_history'))
        self.assertEqual(response.status_code, 200)

    def test_user_search_view_accessible(self):
        """5. Перевірка доступності сторінки пошуку користувачів платформи"""
        response = self.client.get(reverse('users:search_users'))
        self.assertEqual(response.status_code, 200)