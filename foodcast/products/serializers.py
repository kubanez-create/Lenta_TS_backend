from datetime import date

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Forecast, ForecastPoint, Product, Shops

BATCH_FORECAST_TO_CREATE = 200


class ShopsSerializer(serializers.ModelSerializer):
    """Cериализатор обратобки Магазинов ТК."""

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
    """Сериализатор обработки товаров."""

    class Meta:
        model = Product
        fields = (
            "sku",
            "uom",
            "group",
            "category",
            "subcategory",
        )


class FilteredListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        if self.context["request"].query_params.get("date_before") and self.context[
            "request"
        ].query_params.get("date_after"):
            data = data.filter(
                date__lte=self.context["request"].query_params.get("date_before"),
                date__gte=self.context["request"].query_params.get("date_after"),
            )
        return {
            d.date.isoformat(): d.value for d in data.all()
        }

class ForecastPointSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = FilteredListSerializer
        model = ForecastPoint
        exclude = ["id", "forecast"]

    def to_representation(self, data):
        return f"{data.date.isoformat()}", data.value


class ReadForecastSerializer(serializers.ModelSerializer):
    """Сериализатор обработки прогнозов."""
    store = serializers.PrimaryKeyRelatedField(
        queryset=Forecast.objects.all(),
        source='store.title'
    )
    sku = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='sku.sku'
    )
    forecast_date = serializers.DateField()
    sales_units = ForecastPointSerializer(many=True, source="forecast_point")

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
    sales_units = ForecastPointSerializer()


class DataItemSerializer(serializers.Serializer):
    store = serializers.CharField()
    forecast_date = serializers.DateField()
    forecast = ForecastSerializer(many=True, source="forecast_point")

    def validate_forecast_date(self, value):
        dates_created = Forecast.objects.values_list('forecast_date', flat=True)
        if value in dates_created:
            raise serializers.ValidationError('Дата должна быть уникальной')
        return value

    def to_representation(self, obj):
        return {
            "store": obj.store_id,
            "forecast_date": obj.forecast_date,
            "forecast": {
                "sku": obj.sku_id,
                "sales_units": {
                    d.date.isoformat(): d.value for d in obj.forecast_point.all()
                }
            }
        }

    def to_internal_value(self, data):
        return {
            "store": data.get("store"),
            "forecast_date": data.get("forecast_date"),
            "forecast": {
                "sku": data.get("forecast").get("sku"),
                "sales_units": [data.get("forecast").get("sales_units").items()]
            }
        }


class DataSerializer(serializers.Serializer):
    data = serializers.ListField(child=DataItemSerializer())



    def create(self, validated_data):
        print(validated_data)
        forecast_to_create = []

        for item in validated_data['data']:
            store, created = Shops.objects.get_or_create(title=item.get('store'))
            sku = get_object_or_404(Product, sku=str(item.get('forecast').get('sku')))
            new_forecast = Forecast.objects.create(
                store=store,
                forecast_date=str(item.get('forecast_date')),
                sku=sku,
            )
            forecast_points = [
                ForecastPoint(
                    date=date.fromisoformat(dat),
                    value=val,
                    forecast=new_forecast)
                    for dat, val in item.get("forecast").get("sales_units")[0]
            ]
            ForecastPoint.objects.bulk_create(forecast_points, BATCH_FORECAST_TO_CREATE)
            forecast_to_create.append(new_forecast)


        return {'data': forecast_to_create}

