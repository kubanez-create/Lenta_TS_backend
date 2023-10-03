from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import ShopFilter
from .models import Product, Shops
from .serializers import ProductSerializer, ShopsSerializer


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
