import csv
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.core.cache import cache

from ..models import Product, Sales, Shops

User = get_user_model()


class SalesURLsTests(TestCase):
    """Class for testing /sales url."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sale_obj = Sales.objects.create(
            
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(SalesURLsTests.user)
        cache.clear()