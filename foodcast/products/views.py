import ast
import io

import pandas as pd
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .filters import ForecastFilter, ShopFilter
from .models import Forecast, Product, Shops
from .serializers import (
    DataSerializer,
    ProductSerializer,
    ReadForecastSerializer,
    ShopsSerializer,
    StatisticsSerializer
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

    @action(detail=False)
    def excel_forecast_download(self, request, version):
        quseryset = self.filter_queryset(self.get_queryset())
        data = quseryset.values(
            'store__title',
            'sku__sku',
            'forecast_date',
            'forecast_point'
        )
        initial_data = list(data)

        for data in initial_data:
            fc_point_id = data.pop('forecast_point')
            fc_data = ForecastPoint.objects.get(id=fc_point_id)
            data.update(
                {
                    "date": fc_data.date.isoformat(),
                    "value": fc_data.value
                }
            )

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


class StatisticView(APIView):
    """
    View for calculation of statistics.

    * Requires token authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, **kwargs):
        serializer = StatisticsSerializer(request.query_params)

        return Response(serializer.data, status=status.HTTP_200_OK)
