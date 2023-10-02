from datetime import datetime
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.core.cache import cache

from products.models import Product, Sales, Shops, DataPoint

User = get_user_model()


class SalesURLsTests(TestCase):
    """Class for testing /sales url."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(email="a@b.com", password="j7F@")
        cls.product = Product.objects.create(
            sku="fd064933250b0bfe4f926b867b0a5ec8",
            uom="17",
            group="c74d97b01eae257e44aa9d5bade97baf",
            category="1bc0249a6412ef49b07fe6f62e6dc8de",
            subcategory="ca34f669ae367c87f0e75dcae0f61ee5",
        )
        cls.shop = Shops.objects.create(
            title="1aa057313c28fa4a40c5bc084b11d276",
            city="1587965fb4d4b5afe8428a4a024feb0d",
            division="81b4dd343f5880df806d4c5d4a846c64",
            type_format=1,
            loc=1,
            size=19,
            is_active=True,
        )
        cls.sale_obj = Sales.objects.create(
            store=SalesURLsTests.shop,
            SKU=SalesURLsTests.product
        )
        cls.dp1 = DataPoint.objects.create(
            date=datetime.fromisocalendar(2023, 40, 3),
            sales_type=2,
            sales_units=82738,
            sales_units_promo=3,
            sales_rub=3433,
            sales_rub_promo=34,
            sale=SalesURLsTests.sale_obj
        )
        cls.dp2 = DataPoint.objects.create(
            date=datetime.fromisocalendar(2023, 40, 4),
            sales_type=1,
            sales_units=8,
            sales_units_promo=1,
            sales_rub=376,
            sales_rub_promo=34,
            sale=SalesURLsTests.sale_obj
        )
        cls.dp3 = DataPoint.objects.create(
            date=datetime.fromisocalendar(2023, 40, 5),
            sales_type=1,
            sales_units=723,
            sales_units_promo=0,
            sales_rub=78134,
            sales_rub_promo=0,
            sale=SalesURLsTests.sale_obj
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(SalesURLsTests.user)
        cache.clear()

    def test_request_to_sales_url_returns_object(self):
        response = self.authorized_client.get("/api/v1/sales/")
        self.assertEqual(response.status_code, HTTPStatus.OK)