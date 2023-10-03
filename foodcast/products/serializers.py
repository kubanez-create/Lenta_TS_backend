from django.db import transaction
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from .models import Product, Shops, Forecast


BATCH_FORECAST_TO_CREATE = 200


class ShopsSerializer(serializers.ModelSerializer):
    """Cериализатор обратобки Магазинов ТК"""

    class Meta:
        model = Shops
        fields = (
            "title",
            "city",
            "division",
            "type_format",
            "loc",
            "size",
            "is_active",
        )


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор обработки товаров"""

    class Meta:
        model = Product
        fields = (
            "sku",
            "uom",
            "group",
            "category",
            "subcategory",
        )


class ReadForecastSerializer(serializers.ModelSerializer):
    """Сериализатор обработки прогнозов"""
    store = serializers.PrimaryKeyRelatedField(
        queryset=Forecast.objects.all(),
        source='store.title'
    )
    sku = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='sku.sku'
    )
    forecast_date = serializers.DateField()
    sales_units = serializers.JSONField()

    class Meta:
        model = Forecast
        fields = (
            'store',
            'sku',
            'forecast_date',
            'sales_units'
        )


class ForecastSerializer(serializers.Serializer):
    sku = serializers.CharField()
    sales_units = serializers.JSONField()


class DataItemSerializer(serializers.Serializer):
    store = serializers.CharField()
    forecast_date = serializers.DateField()
    forecast = ForecastSerializer()

    def validate_forecast_date(self, value):
        dates_created = Forecast.objects.values_list('forecast_date', flat=True)
        if value in dates_created:
            raise serializers.ValidationError('Дата должна быть уникальной')
        return value


class DataSerializer(serializers.Serializer):
    data = serializers.ListField(child=DataItemSerializer())

    def create(self, validated_data):
        print(validated_data)
        # data = validated_data.pop('data')
        forecast_to_create = []

        for item in validated_data['data']:
            store, created = Shops.objects.get_or_create(title=item.get('store'))
            sku = get_object_or_404(Product, sku=str(item.get('forecast').get('sku')))
            bulk_data = Forecast(
                store=store,
                forecast_date=str(item.get('forecast_date')),
                sku=sku,
                sales_units=str(item.get('forecast').get('sales_units'))
            )
            forecast_to_create.append(bulk_data)

        Forecast.objects.bulk_create(forecast_to_create, BATCH_FORECAST_TO_CREATE)

        return {'data': forecast_to_create}

