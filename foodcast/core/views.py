from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.serializers import SalesSerializer
from products.models import Sales

class SalesView(ListAPIView):
    """
    View to get historic numbers for sales.

    * Requires token authentication.
    """
    serializer_class = SalesSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['SKU__group', 'SKU__category', 'SKU__subcategory']
    permission_classes = [IsAuthenticated]
    queryset = Sales.objects.all()
