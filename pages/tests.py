from django.test import SimpleTestCase
from django.urls import reverse, resolve

from .views import HomePageView


class HomePageTest(SimpleTestCase):
    """тест: домашняя странца"""

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        """тест: статус ответа домашней страницы"""
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        """тест: используется верный шаблон"""
        self.assertTemplateUsed(self.response, 'home.html')

    def test_homepage_contains_correct_html(self):
        """тест: домашняя страница содержит правильный html"""
        self.assertContains(self.response, 'Homepage')

    def test_homepage_does_not_contain_incorrect_html(self):
        """тест: домашняя страница не содержит лишнего html"""
        self.assertNotContains(self.response, 'Some random text')

    def test_homepage_url_resolves_homepageview(self):
        """тест: проверяет что url использует нужное представление"""
        view = resolve('/')
        self.assertEqual(
            view.func.__name__,
            HomePageView.as_view().__name__
        )