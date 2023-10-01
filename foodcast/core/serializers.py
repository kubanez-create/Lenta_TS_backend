# from django.shortcuts import get_object_or_404
from rest_framework import serializers

from products.models import Sales, DataPoint


class DataPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPoint
        exclude = ["id"]


class SalesSerializer(serializers.ModelSerializer):
    fact = DataPointSerializer(many=True, source="datapoint")

    class Meta:
        model = Sales
        fields = ("store", "SKU", "fact")
