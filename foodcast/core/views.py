from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from core.serializers import SalesSerializer
from products.models import Sales
from products.filters import SalesFilter


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
