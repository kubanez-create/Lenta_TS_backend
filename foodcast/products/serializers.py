from rest_framework import serializers

from .models import (
    ProductGroup,
    ProductCategory,
    ProductSubCategory,
    Product,
    Shops
)


class ShopsSerializer(serializers.ModelSerializer):
    """Cериализатор обратобки Магазинов ТК"""
    class Meta:
        model = Shops
        fields = (
            'title',
            'city',
            'division',
            'type_format',
            'loc',
            'size',
            'is_active'
        )


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор обработки Групп товаров"""
    class Meta:
        model = ProductGroup
        fields = ('title',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор обработки Категорий товаров"""
    class Meta:
        model = ProductCategory
        fields = ('title', 'group')


class SubCategorySerializer(serializers.ModelSerializer):
    """Сериализатор обработки Категорий товаров"""
    class Meta:
        model = ProductSubCategory
        fields = ('title', 'category')


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор обработки товаров"""
    group = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    subcategory = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'sku',
            'uom',
            'group',
            'category',
            'subcategory',
        )

    def get_group(self, obj):
        return obj.group.title if obj.group else None

    def get_category(self, obj):
        return obj.category.title if obj.category else None

    def get_subcategory(self, obj):
        return obj.subcategory.title if obj.subcategory else None
