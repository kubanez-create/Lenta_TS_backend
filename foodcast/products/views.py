from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import ShopFilter
from .models import Shops, ProductGroup, ProductCategory, ProductSubCategory, Product
from .serializers import ShopsSerializer, GroupSerializer, CategorySerializer, SubCategorySerializer, ProductSerializer


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


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = ProductGroup.objects.all()
    permission_classes = (IsAuthenticated,)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = ProductCategory.objects.all()
    permission_classes = (IsAuthenticated,)


class SubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer
    queryset = ProductSubCategory.objects.all()
    permission_classes = (IsAuthenticated,)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        response_data = {'data': serializer.data}
        return Response(response_data)
