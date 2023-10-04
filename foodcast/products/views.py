from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
import pandas as pd
import io
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import ShopFilter
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
        data = quseryset.values('store__title', 'sku__sku', 'forecast_date', 'sales_units')

        df = pd.DataFrame(data)
        excel_file = io.BytesIO()
        df.to_excel(excel_file, index=False, sheet_name=f'forecast_export')

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="forecast_data.xlsx"'
        excel_file.seek(0)
        response.write(excel_file.read())

        return response


"""    def create(self, request, *args, **kwargs):
        serializer = DataSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""