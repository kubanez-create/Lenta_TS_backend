from datetime import date

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse
from products.models import Forecast, ForecastPoint, Product, Shops

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
        self.guest_client = Client()
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
        print(response, response.content)
        self.assertEquals(
            response.get('Content-Disposition'),
            "attachment; filename=forecast_data.xlsx"
        )
