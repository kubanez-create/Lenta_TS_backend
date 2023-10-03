from datetime import datetime
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from products.models import DataPoint, Product, Sales, Shops

User = get_user_model()


class SalesURLsTests(TestCase):
    """Class for testing /sales url."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(email="a@b.com", password="j7F@")

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(SalesURLsTests.user)
        cache.clear()

    def test_authorized_user_can_reach_sales(self):
        response = self.authorized_client.get("/api/v1/sales/")
        self.assertEqual(response.status_code, HTTPStatus.OK.value)

    def test_unauthorized_user_cant_reach_sales(self):
        response = self.guest_client.get("/api/v1/sales/")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED.value)
