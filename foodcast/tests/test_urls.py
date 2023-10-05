from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase

User = get_user_model()


class SalesURLsTests(TestCase):
    """Class for testing /sales url."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(email="a@b.com", password="j7F@")
        cls.urls = {
            "sales": "/api/v1/sales/",
            "shops": "/api/v1/shops/",
            "product": "/api/v1/product/",
            "forecast": "/api/v1/forecast/",
        }

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(SalesURLsTests.user)
        cache.clear()

    def test_authorized_user_can_reach_urls(self):
        for name, url in SalesURLsTests.urls.items():
            with self.subTest(url_name=name):
                response = self.authorized_client.get(url)
                print(response)
                self.assertEqual(response.status_code, HTTPStatus.OK.value)

    def test_unauthorized_user_cannot_reach_urls(self):
        for name, url in SalesURLsTests.urls.items():
            with self.subTest(url_name=name):
                response = self.guest_client.get(url)
                self.assertEqual(
                    response.status_code, HTTPStatus.UNAUTHORIZED.value)
