from core.serializers import SalesSerializer
from django_filters.rest_framework import DjangoFilterBackend
from products.filters import SalesFilter
from products.models import Sales
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated


class SalesView(ListAPIView):
    """
    View to get historic numbers for sales.

    * Requires token authentication.
    """

    serializer_class = SalesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalesFilter
    permission_classes = [IsAuthenticated]
    queryset = Sales.objects.all()
