from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from . import services

from django.contrib.auth.models import User
from django.urls import reverse
from .models import BookmarkedProfile


class ServiceTests(TestCase):
    def test_get_user_returns_username(self):
        data = services.get_user("torvalds")
        self.assertEqual(data["username"], "torvalds")

    def test_user_not_found(self):
        with self.assertRaises(services.UserNotFound):
            services.get_user("this-user-does-not-exist-98765")

    def test_invalid_username(self):
        with self.assertRaises(services.UserNotFound):
            services.get_user("bad name!!")


class ViewTests(TestCase):
    def setUp(self):
        User.objects.create_user("student", password="pass12345")

    def test_search_page_loads(self):
        response = self.client.get(reverse("search"))
        self.assertEqual(response.status_code, 200)

    def test_search_unknown_user_shows_message(self):
        response = self.client.get(reverse("search"), {"q": "this-user-does-not-exist-98765"})
        messages = [str(m) for m in response.context["messages"]]
        self.assertIn("No GitHub user with that username.", messages)

    def test_bookmark_requires_login(self):
        response = self.client.post(reverse("bookmark", args=["torvalds"]))
        self.assertEqual(response.status_code, 302)

    def test_bookmark_twice_creates_one_row(self):
        self.client.login(username="student", password="pass12345")
        self.client.post(reverse("bookmark", args=["torvalds"]))
        self.client.post(reverse("bookmark", args=["torvalds"]))
        self.assertEqual(BookmarkedProfile.objects.count(), 1)