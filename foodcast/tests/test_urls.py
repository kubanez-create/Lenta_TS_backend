from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class URLsTests(TestCase):
    """Class for testing application urls."""

    url_without_version = "/api/sales/"
    url_with_wrong_version = "/api/v4/sales"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(email="a@b.com")
        cls.urls = {
            "sales": reverse("core:sales", kwargs={"version": "v1"}),
            "product": reverse(
                "products:product-list", kwargs={"version": "v1"}
            ),
            "forecast": reverse(
                "products:forecast-list", kwargs={"version": "v1"}
            ),
            "forecast_excel": reverse(
                "products:statistics", kwargs={"version": "v1"}
            ),
        }

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(URLsTests.user)
        cache.clear()


    def test_authorized_user_can_reach_urls(self):
        for name, url in URLsTests.urls.items():
            with self.subTest(url_name=name):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK.value)

    def test_unauthorized_user_cannot_reach_urls(self):
        for name, url in URLsTests.urls.items():
            with self.subTest(url_name=name):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED.value)

    def test_version_outside_1_or_2_not_found(self):
        response = self.authorized_client.get(self.url_with_wrong_version)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_url_without_version_is_not_found(self):
        response = self.authorized_client.get(self.url_without_version)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
