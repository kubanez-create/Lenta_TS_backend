from django.test import TestCase
from django.contrib.auth import get_user_model

from products.models import (
    Product,
    Shops,
)


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
    ...
