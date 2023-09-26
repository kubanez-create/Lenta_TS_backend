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
