from rest_framework import serializers

from .models import (
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


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор обработки товаров"""
    class Meta:
        model = Product
        fields = (
            'sku',
            'uom',
            'group',
            'category',
            'subcategory',
        )
