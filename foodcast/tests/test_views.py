import json
from datetime import date

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse
from products.models import (
    DataPoint,
    Forecast,
    ForecastPoint,
    Product,
    Sales,
    Shops
)

User = get_user_model()


class ForecastViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(email="a@b.com")
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
        cls.forecast = Forecast.objects.create(
            store=ForecastViewTests.shop,
            sku=ForecastViewTests.product,
            forecast_date=date.today()
        )
        cls.p1 = ForecastPoint.objects.create(
            date=date(2023, 9, 3),
            value=3,
            forecast=ForecastViewTests.forecast,
        )
        cls.p2 = ForecastPoint.objects.create(
            date=date(2023, 9, 4),
            value=2,
            forecast=ForecastViewTests.forecast,
        )
        cls.p3 = ForecastPoint.objects.create(
            date=date(2023, 9, 5),
            value=1,
            forecast=ForecastViewTests.forecast,
        )
        cls.p4 = ForecastPoint.objects.create(
            date=date(2023, 9, 6),
            value=12,
            forecast=ForecastViewTests.forecast,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(ForecastViewTests.user)
        cache.clear()

    def test_forecast_vies_can_return_excel_file(self):
        """Запрос на /forecast/get/excel returns a file."""
        response = self.authorized_client.get(
            reverse(
                "products:forecast-excel-forecast-download",
                kwargs={"version": "v1"},
            )
        )
        self.assertEquals(
            response.get('Content-Disposition'),
            "attachment; filename=forecast_data.xlsx"
        )


class StatisticsViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(email="a@b.com")
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
        cls.forecast = Forecast.objects.create(
            store=StatisticsViewTests.shop,
            sku=StatisticsViewTests.product,
            forecast_date=date.today()
        )
        cls.p1 = ForecastPoint.objects.create(
            date=date(2023, 9, 3),
            value=3,
            forecast=StatisticsViewTests.forecast,
        )
        cls.p2 = ForecastPoint.objects.create(
            date=date(2023, 9, 4),
            value=2,
            forecast=StatisticsViewTests.forecast,
        )
        cls.p3 = ForecastPoint.objects.create(
            date=date(2023, 9, 5),
            value=1,
            forecast=StatisticsViewTests.forecast,
        )
        cls.sale_obj = Sales.objects.create(
            store=StatisticsViewTests.shop, SKU=StatisticsViewTests.product
        )
        cls.dp1 = DataPoint.objects.create(
            date=date(2023, 9, 3),
            sales_type=2,
            sales_units=82738,
            sales_units_promo=3,
            sales_rub=3433,
            sales_rub_promo=34,
            sale=StatisticsViewTests.sale_obj,
        )
        cls.dp2 = DataPoint.objects.create(
            date=date(2023, 9, 4),
            sales_type=1,
            sales_units=8,
            sales_units_promo=1,
            sales_rub=376,
            sales_rub_promo=34,
            sale=StatisticsViewTests.sale_obj,
        )
        cls.dp3 = DataPoint.objects.create(
            date=date(2023, 9, 5),
            sales_type=1,
            sales_units=723,
            sales_units_promo=0,
            sales_rub=78134,
            sales_rub_promo=0,
            sale=StatisticsViewTests.sale_obj,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(StatisticsViewTests.user)
        cache.clear()

    def test_statistic_returns_3_vectors(self):
        """Запрос на /forecast/get/excel returns a file."""
        response = self.authorized_client.get(
            reverse(
                "products:statistics",
                kwargs={"version": "v1"},
            )
        )
        self.assertEquals(
            json.loads(response.content).get("sales_and_forecast_objects")[0],
            {
                "store":"1aa057313c28fa4a40c5bc084b11d276",
                "sku":"fd064933250b0bfe4f926b867b0a5ec8",
                "date":"2023-09-03",
                "diff":82738,
                "wape":1.0
            }
        )