from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase

User = get_user_model()


class URLsTests(TestCase):
    """Class for testing application urls."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(email="a@b.com")
        cls.urls = {
            "sales": "/api/v1/sales/",
            "shops": "/api/v1/shops/",
            "product": "/api/v1/product/",
            "forecast": "/api/v1/forecast/",
        }

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(URLsTests.user)
        cache.clear()

    # Test throws an error:
    # FAIL: test_authorized_user_can_reach_urls (tests.test_urls.URLsTests) (url_name='shops')
    # ----------------------------------------------------------------------
    # Traceback (most recent call last):
    # File "/home/kubanez/Dev/Lenta_TS_backend/foodcast/tests/test_urls.py", line 35, in test_authorized_user_can_reach_urls
     #   self.assertEqual(response.status_code, HTTPStatus.OK.value)
    # AssertionError: 404 != 200
    def test_authorized_user_can_reach_urls(self):
        for name, url in URLsTests.urls.items():
            with self.subTest(url_name=name):
                response = self.authorized_client.get(url)
                print(response.request)
                self.assertEqual(response.status_code, HTTPStatus.OK.value)

    def test_unauthorized_user_cannot_reach_urls(self):
        for name, url in URLsTests.urls.items():
            with self.subTest(url_name=name):
                response = self.guest_client.get(url)
                self.assertEqual(
                    response.status_code, HTTPStatus.UNAUTHORIZED.value)
