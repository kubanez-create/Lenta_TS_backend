import json
from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from products.models import DataPoint, Forecast, Product, Sales, Shops

User = get_user_model()


class ProductModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = Product.objects.create(
            sku="fd064933250b0bfe4f926b867b0a5ec8",
            uom="17",
            group="c74d97b01eae257e44aa9d5bade97baf",
            category="1bc0249a6412ef49b07fe6f62e6dc8de",
            subcategory="ca34f669ae367c87f0e75dcae0f61ee5",
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        product = ProductModelTest.product
        field_verboses = {
            "sku": "SKU продукта",
            "uom": "UOM еденица измерения",
            "group": "Группа товаров",
            "category": "Категория товаров",
            "subcategory": "Подкатегория товаров",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    product._meta.get_field(field).verbose_name, expected_value
                )

    def test_str_representation(self):
        self.assertEqual(
            str(ProductModelTest.product),
            "SKU - fd064933250b0bfe4f926b867b0a5ec8, ед. изм - 17",
        )

    def sku_id_a_primary_key(self):
        self.assertEqual(
            ProductModelTest.product.pk, "fd064933250b0bfe4f926b867b0a5ec8"
        )


class ShopsModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.shop = Shops.objects.create(
            title="1aa057313c28fa4a40c5bc084b11d276",
            city="1587965fb4d4b5afe8428a4a024feb0d",
            division="81b4dd343f5880df806d4c5d4a846c64",
            type_format=1,
            loc=1,
            size=19,
            is_active=True,
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        shop = ShopsModelTest.shop
        field_verboses = {
            "title": "Название",
            "city": "Город",
            "division": "Дивизион",
            "type_format": "Тип Формата",
            "loc": "Локация",
            "size": "Размер",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    shop._meta.get_field(field).verbose_name, expected_value
                )

    def test_str_representation(self):
        self.assertEqual(
            str(ShopsModelTest.shop),
            (
                "Магазин 1aa057313c28fa4a40c5bc084b11d276, г. "
                "1587965fb4d4b5afe8428a4a024feb0d, статус - True"
            ),
        )

    def sku_id_a_primary_key(self):
        self.assertEqual(ShopsModelTest.shop.pk, "1aa057313c28fa4a40c5bc084b11d276")


class DataPointModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
            store=DataPointModelTest.shop, SKU=DataPointModelTest.product
        )
        cls.point = DataPoint.objects.create(
            date = date.today(),
            sales_type = 1,
            sales_units = 4,
            sales_units_promo = 1,
            sales_rub = 1433,
            sales_rub_promo = 98,
            sale = DataPointModelTest.sale_obj
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        datapoint = DataPointModelTest.point
        field_verboses = {
            "date": "Дата",
            "sales_type": "Тип",
            "sales_units": "Продажи, ед.изм",
            "sales_units_promo": "Продажи в акцию, ед.изм",
            "sales_rub": "Продажи, руб.",
            "sales_rub_promo": "Продажи в акцию, руб.",
            "sale": "Реализация"
        }

        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    datapoint._meta.get_field(field).verbose_name, expected_value
                )


class SalesModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
            store=DataPointModelTest.shop, SKU=DataPointModelTest.product
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        deal = SalesModelTest.sale_obj
        field_verboses = {
            "store": "ТЦ",
            "SKU": "SKU"
        }

        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    deal._meta.get_field(field).verbose_name, expected_value
                )


class ForecastModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
            store=ForecastModelTest.shop,
            sku=ForecastModelTest.product,
            forecast_date=date.today(),
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        fc = ForecastModelTest.forecast
        field_verboses = {
            "store": "ТЦ",
            "sku": "SKU",
            "forecast_date": "Дата прогноза",
        }

        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    fc._meta.get_field(field).verbose_name, expected_value
                )