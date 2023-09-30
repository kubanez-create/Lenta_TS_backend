import csv
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.core.cache import cache

from ..models import Group, Post

User = get_user_model()


class SalesURLsTests(TestCase):
    """Class for testing /sales url."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        entry = (
            "st_id", "pr_sku_id", "date	pr_sales_type_id",	"pr_sales_in_units", "pr_promo_sales_in_units",	"pr_sales_in_rub",	"pr_promo_sales_in_rub\n"
            "c81e728d9d4c2f636f067f89cc14862c",	"c7b711619071c92bef604c7ad68380dd",	"10/20/2022", "1", "5",	"5", "825",	"825\n"

        )
        with open("mock.csv", "x") as f:
            writer = csv.writer(f)
            writer.writerows(entry)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(SalesURLsTests.user)
        cache.clear()