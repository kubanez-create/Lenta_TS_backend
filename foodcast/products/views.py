import ast

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
import pandas as pd
import io
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import ForecastFilter, ShopFilter
from .models import Forecast, Product, Shops
from .serializers import (
    DataSerializer, ProductSerializer, ReadForecastSerializer, ShopsSerializer
)


@action(detail=True, methods=['get'])
class ShopsViewSet(viewsets.ModelViewSet):
    serializer_class = ShopsSerializer
    queryset = Shops.objects.all()
    filter_backends = [DjangoFilterBackend,]
    filterset_class = ShopFilter
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        response_data = {'data': serializer.data}
        return Response(response_data)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        response_data = {'data': serializer.data}
        return Response(response_data)


class ForecastViewSet(viewsets.ModelViewSet):
    queryset = Forecast.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = ForecastFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadForecastSerializer
        return DataSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        response_data = {'data': serializer.data}
        return Response(response_data)

    @action(detail=False, methods=['get'])
    def excel_forecast_download(self, request):
        quseryset = self.get_queryset()
        data = quseryset.values(
            'store__title',
            'sku__sku',
            'forecast_date',
            'sales_units')
        initial_data = list(data)

        for data in initial_data:
            sales_units_str = data.pop('sales_units')
            sales_units_dict = ast.literal_eval(sales_units_str)
            data.update(sales_units_dict)

        df = pd.DataFrame(initial_data)
        df = df.rename(columns={
            'store__title': 'Магазин',
            'sku__sku': 'SKU',
            'forecast_date': 'Дата Прогноза'})
        excel_file = io.BytesIO()
        df.to_excel(
            excel_file,
            index=False,
            sheet_name='forecast_export',
            startrow=2
        )

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="forecast_data.xlsx"'
        excel_file.seek(0)
        response.write(excel_file.read())

        return response
