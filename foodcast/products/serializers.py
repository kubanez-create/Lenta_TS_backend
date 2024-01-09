from datetime import date

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import DataPoint, Forecast, ForecastPoint, Product, Sales, Shops

BATCH_FORECAST_TO_CREATE = 200

def wape(actual: int, pred: int) -> int:
    if actual == 0:
        return 0
    numerator = abs(actual - pred)
    return numerator / abs(actual)

class ShopsSerializer(serializers.ModelSerializer):
    """Cериализатор обработки магазинов торговой сети."""

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


class StatisticsSerializer(serializers.Serializer):
    sales_and_forecast_objects = serializers.SerializerMethodField(
        read_only=True)

    def get_sales_and_forecast_objects(self, obj):
        """Get historic sales and forecast values.

        In order to show statistics we need to first filter all
        ForecastPoint and DataPoint (historic sales) objects by
        store, group, category, subcategory and period and then
        return a neat json list with our data. 
        """
        store = obj.get("store")
        group = obj.get("group")
        category = obj.get("category")
        subcategory = obj.get("subcategory")
        date_before = obj.get("date_before")
        date_after = obj.get("date_after")

        fc_queryset = ForecastPoint.objects.all()
        sale_queryset = DataPoint.objects.all()
        if store:
            fc_queryset = fc_queryset.filter(forecast__store=store)
            sale_queryset = sale_queryset.filter(sale__store=store)
        if group:
            fc_queryset = fc_queryset.filter(forecast__sku__group=group)
            sale_queryset = sale_queryset.filter(sale__SKU__group=group)
        if category:
            fc_queryset = fc_queryset.filter(forecast__sku__category=category)
            sale_queryset = sale_queryset.filter(sale__SKU__category=category)
        if subcategory:
            fc_queryset = fc_queryset.filter(
                forecast__sku__subcategory=subcategory
            )
            sale_queryset = sale_queryset.filter(
                sale__SKU__subcategory=subcategory
            )

        if date_after and date_before:
            fc_queryset = fc_queryset.filter(
                date__lte=date_before, date__gte=date_after
            )
            sale_queryset = sale_queryset.filter(
                date__lte=date_before, date__gte=date_after
            )
        fc_queryset = list(fc_queryset.order_by("date").values())
        sale_queryset = list(sale_queryset.order_by("date").values())

        # in case we have only predicted (or actual) value for some day
        # we keep present value and put None in place of the other

        merged_queryset = []
        while fc_queryset and sale_queryset:
            if fc_queryset[-1]["date"] == sale_queryset[-1]["date"]:
                merged_queryset.append(
                    (fc_queryset.pop(), sale_queryset.pop())
                )
            elif fc_queryset[-1]["date"] > sale_queryset[-1]["date"]:
                merged_queryset.append((fc_queryset.pop(), None))
            else:
                merged_queryset.append((None, sale_queryset.pop()))

        if fc_queryset:
            merged_queryset.append((fc_queryset.pop(), None))
        if sale_queryset:
            merged_queryset.append((None, sale_queryset.pop()))

        result = []
        for fc, sale in merged_queryset[::-1]:
            if fc and sale:
                result.append(
                    {
                        "store": Forecast.objects.get(id=fc["forecast_id"]).store_id,
                        "sku": Forecast.objects.get(id=fc["forecast_id"]).sku.sku,
                        "date": fc.get("date"),
                        "diff": abs(
                            fc.get("value") - (sale.get("sales_units")
                            + sale.get("sales_units_promo"))
                        ),
                        "wape": round(wape(
                            (sale.get("sales_units") + sale.get("sales_units_promo")),
                             fc.get("value")
                        ), ndigits=3)
                    }
                )
            if fc:
                result.append(
                    {
                        "store": Forecast.objects.get(id=fc["forecast_id"]).store_id,
                        "sku": Forecast.objects.get(id=fc["forecast_id"]).sku.sku,
                        "date": fc["date"],
                        "diff": None,
                        "wape": None
                    }
                )
            if sale:
                result.append(
                    {
                        "store": Sales.objects.get(id=sale["sale_id"]).store_id,
                        "sku": Sales.objects.get(id=sale["sale_id"]).SKU.sku,
                        "date": sale["date"],
                        "diff": None,
                        "wape": None
                    }
                )

        return result
