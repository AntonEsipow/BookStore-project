from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from .models import Book, Review


class BookTests(TestCase):
    """Тест книг"""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='reviewuser',
            email='reviewuser@mail.com',
            password='testpass123'
        )

        self.special_permission = Permission.objects.get(
            codename='special_status'
        )

        self.book = Book.objects.create(
            title='Harry Potter',
            author='JK Rowling',
            price='40.00',
        )

        self.review = Review.objects.create(
            book=self.book,
            review='Great review',
            author=self.user,
        )

    def test_book_listing(self):
        """тест: отображения книги"""
        self.assertEqual(f'{self.book.title}', 'Harry Potter')
        self.assertEqual(f'{self.book.author}', 'JK Rowling')
        self.assertEqual(f'{self.book.price}', '40.00')

    def test_book_list_view_for_logged_in_user(self):
        """тест: отображения списка книг для авторизированного пользователя"""
        self.client.login(email='reviewuser@mail.com', password='testpass123')
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Harry Potter')
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_detail_view_for_logged_out_user(self):
        """тест: отображения деталей книги для не авторизированного пользователя"""
        self.client.logout()
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '%s?next=/books/' % (reverse('account_login')))
        response = self.client.get(
            '%s?next=/books/' % (reverse('account_login')))
        self.assertContains(response, 'Log In')

    def test_book_detail_view_with_permissions(self):
        """тест: просмотр деталей книги с разрешениями"""
        self.client.login(email='reviewuser@email.com', password='testpass123')
        self.user.user_permissions.add(self.special_permission)
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Harry Potter')
        self.assertContains(response, 'Great review')
        self.assertTemplateUsed(response, 'books/book_detail.html')