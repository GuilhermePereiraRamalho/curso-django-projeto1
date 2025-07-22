from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class AuthorLogoutTes(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.client.login(
            username='testuser',
            password='testpassword'
        )

        response = self.client.get(
            reverse('authors:logout'),
            follow=True
        )

        self.assertIn(
            "Invalid logout request.",
            response.content.decode('utf-8')
        )

    def test_user_tries_to_logout_another_user(self):
        User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.client.login(
            username='testuser',
            password='testpassword'
        )

        response = self.client.post(
            reverse('authors:logout'),
            data={'username': 'anotheruser'},
            follow=True
        )

        self.assertIn(
            "Invalid logout user.",
            response.content.decode('utf-8')
        )

    def test_user_can_logout_successfully(self):
        User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.client.login(
            username='testuser',
            password='testpassword'
        )

        response = self.client.post(
            reverse('authors:logout'),
            data={'username': 'testuser'},
            follow=True
        )

        self.assertIn(
            "Logged out successfully.",
            response.content.decode('utf-8')
        )
