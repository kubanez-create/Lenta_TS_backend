import json
from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.core.cache import cache
from django.urls import reverse

from products.models import Product, Sales, Shops, DataPoint

User = get_user_model()


class SalesURLsTests(TestCase):
    """Class for testing /sales filters."""

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
        cls.product2 = Product.objects.create(
            sku="71c9661741caf40a92a32d1cc8206c04",
            uom="17",
            group="c74d97b01eae257e44aa9d5bade97baf",
            category="c559da2ba967eb820766939a658022c8",
            subcategory="e06f5ed77191826c212c30722f2cc5a2",
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
            store=SalesURLsTests.shop, SKU=SalesURLsTests.product
        )
        cls.sale_obj2 = Sales.objects.create(
            store=SalesURLsTests.shop, SKU=SalesURLsTests.product2
        )
        cls.dp1 = DataPoint.objects.create(
            date=datetime.fromisocalendar(2023, 40, 3),
            sales_type=2,
            sales_units=82738,
            sales_units_promo=3,
            sales_rub=3433,
            sales_rub_promo=34,
            sale=SalesURLsTests.sale_obj,
        )
        cls.dp2 = DataPoint.objects.create(
            date=datetime.fromisocalendar(2023, 40, 4),
            sales_type=1,
            sales_units=8,
            sales_units_promo=1,
            sales_rub=376,
            sales_rub_promo=34,
            sale=SalesURLsTests.sale_obj,
        )
        cls.dp3 = DataPoint.objects.create(
            date=datetime.fromisocalendar(2023, 40, 5),
            sales_type=1,
            sales_units=723,
            sales_units_promo=0,
            sales_rub=78134,
            sales_rub_promo=0,
            sale=SalesURLsTests.sale_obj,
        )
        cls.dp4 = DataPoint.objects.create(
            date=datetime.fromisocalendar(2023, 40, 4),
            sales_type=1,
            sales_units=18,
            sales_units_promo=18,
            sales_rub=3760,
            sales_rub_promo=3760,
            sale=SalesURLsTests.sale_obj2,
        )
        cls.dp5 = DataPoint.objects.create(
            date=datetime.fromisocalendar(2023, 40, 7),
            sales_type=2,
            sales_units=716,
            sales_units_promo=55,
            sales_rub=13413,
            sales_rub_promo=238,
            sale=SalesURLsTests.sale_obj2,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(SalesURLsTests.user)
        cache.clear()

    def test_sales_view_returns_correct_obj_without_filters(self):
        """Запрос на /sales без фильтров возвращает корректный объект."""
        response = self.authorized_client.get(
            reverse("core:sales", kwargs={"version": "v1"})
        )
        response_json = json.loads(response.content)[0]
        self.assertEqual(response_json["store"], SalesURLsTests.shop.title)
        self.assertEqual(response_json["SKU"], SalesURLsTests.product.sku)

    def test_sales_view_returns_correct_obj_with_store_filter(self):
        """Запрос на /sales с фильтром на ТЦ возвращает корректный объект."""
        response = self.authorized_client.get(
            reverse("core:sales", kwargs={"version": "v1"})
            + f"store={SalesURLsTests.shop.title}"
        )
        response_json = json.loads(response.content)[0]
        self.assertEqual(response_json["store"], SalesURLsTests.shop.title)
        self.assertEqual(response_json["SKU"], SalesURLsTests.product.sku)

    def test_sales_view_returns_correct_obj_with_group_filter(self):
        """Запрос на /sales с фильтром по группе выдает корректный объект."""
        response = self.authorized_client.get(
            reverse("core:sales", kwargs={"version": "v1"})
            + f"?group={SalesURLsTests.product.group}"
        )
        response_json = json.loads(response.content)[0]
        self.assertEqual(response_json["SKU"], SalesURLsTests.product.sku)

    def test_sales_view_returns_empty_list_for_wrong_group(self):
        """Запрос на /sales с фильтром по группе возвращает пустой лист.

        Если мы фильтруем с несуществующей группой мы должны получить
        пустой лист.
        """
        response = self.authorized_client.get(
            reverse("core:sales", kwargs={"version": "v1"}) + "?group=kjh445"
        )
        self.assertEqual(json.loads(response.content), [])

    def test_sales_view_returns_correct_datapoints_by_date(self):
        """Запрос на /sales с фильтром по дате выдает верные данные.

        Когда мы фильтруем по дате начала и окончания периода
        date_after and date_before мы должны получить только
        данные, которые находятся внутри временного диапазона
        включая даты начала и окончания."""
        response = self.authorized_client.get(
            (
                reverse("core:sales", kwargs={"version": "v1"})
                + f"?date_before={datetime.fromisocalendar(2023, 40, 6).date()}"
                + f"&date_after={datetime.fromisocalendar(2023, 40, 4).date()}"
            )
        )
        response_json = json.loads(response.content)[0]
        self.assertEqual(len(response_json["fact"]), 2)

    def test_sales_filtered_by_group_return_two_objects(self):
        """Запрос на /sales с фильтром по группе выдает оба объекта.

        В случае, если у нас два товара в продаже с одинаковой группой
        мы должны видеть оба в выдаче, при фильтрации по группе.
        """
        response = self.authorized_client.get(
            reverse("core:sales", kwargs={"version": "v1"})
            + f"?group={SalesURLsTests.product.group}"
        )
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 2)
