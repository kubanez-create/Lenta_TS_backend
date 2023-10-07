from products.models import DataPoint, Sales
from rest_framework import serializers


class FilteredListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        if self.context["request"].query_params.get("date_before") and self.context[
            "request"
        ].query_params.get("date_after"):
            data = data.filter(
                date__lte=self.context["request"].query_params.get("date_before"),
                date__gte=self.context["request"].query_params.get("date_after"),
            )
        return super(FilteredListSerializer, self).to_representation(data)


class DataPointSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = FilteredListSerializer
        model = DataPoint
        exclude = ["id"]


class SalesSerializer(serializers.ModelSerializer):
    fact = DataPointSerializer(many=True, source="datapoint")

    class Meta:
        model = Sales
        fields = ("store", "SKU", "fact")
