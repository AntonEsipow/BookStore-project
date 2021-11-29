from django.contrib.auth import get_user_model
from django.test import TestCase


class CustomUserTest(TestCase):
    """Тест: кастомная модель пользователя"""

    def test_create_user(self):
        """тест: создания пользователя"""
        User = get_user_model()
        user = User.objects.create_user(
            username='will',
            email='will@email.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'will')
        self.assertEqual(user.email, 'will@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """тест: создание суперпользователя"""
        User = get_user_model()
        user = User.objects.create_superuser(
            username='superadmin',
            email='some@mail.com',
            password='random333pass'
        )
        self.assertEqual(user.username, 'superadmin')
        self.assertEqual(user.email, 'some@mail.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)