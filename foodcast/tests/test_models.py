from django.test import TestCase
from products.models import (
    Product,
    ProductCategory,
    ProductGroup,
    ProductSubCategory,
    Shops,
)


class ProductGroupModelTest(TestCase):
    def test_str_representation(self):
        group = ProductGroup(title="Test Group")
        self.assertEqual(str(group), "Группа товаров - Test Group")


class ProductCategoryModelTest(TestCase):
    def test_str_representation(self):
        group = ProductGroup(title="Test Group")
        category = ProductCategory(title="Test Category", group=group)
        self.assertEqual(str(category), "Категория - Test Category")


class ProductSubCategoryModelTest(TestCase):
    def test_str_representation(self):
        group = ProductGroup(title="Test Group")
        category = ProductCategory(title="Test Category", group=group)
        subcategory = ProductSubCategory(
            title="Test Subcategory",
            category=category
        )
        self.assertEqual(str(subcategory), "Подкатегория - Test Subcategory")


class ProductModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        group = ProductGroup.objects.create(title="Test Group")
        category = ProductCategory.objects.create(
            title="Test Category", group=group
        )
        subcategory = ProductSubCategory.objects.create(
            title="Test Subcategory", category=category
        )
        cls.product = Product.objects.create(
            sku="TEST001",
            uom="Each",
            group=group,
            category=category,
            subcategory=subcategory,
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        product = ProductModelTest.product
        field_verboses = {
            "sku": "SKU продукта",
            "uom": "UOM еденица измерения",
            "group": "Группа",
            "category": "Категория",
            "subcategory": "Подкатегория",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    product._meta.get_field(field).verbose_name, expected_value
                )

    def test_str_representation(self):
        self.assertEqual(
            str(ProductModelTest.product),
            "SKU - TEST001, ед. изм - Each"
        )


class ShopsModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.shop = Shops.objects.create(
            title="Test Shop",
            city="Test City",
            division="Test Division",
            type_format=1,
            loc=1,
            size=100,
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
            "Магазин Test Shop, г. Test City, статус - True",
        )