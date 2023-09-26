import django_filters
from django_filters import FilterSet
from rest_framework.exceptions import NotFound

from .models import Shops


class ShopFilter(FilterSet):
    title = django_filters.CharFilter(lookup_expr='exact')
    city = django_filters.CharFilter(lookup_expr='exact')
    division = django_filters.CharFilter(lookup_expr='exact')
    type_format = django_filters.CharFilter(lookup_expr='exact')
    loc = django_filters.CharFilter(lookup_expr='exact')
    size = django_filters.CharFilter(lookup_expr='exact')
    is_active = django_filters.CharFilter(lookup_expr='exact')

    def filter_queryset(self, queryset):
        filtered_quaeryset = super().filter_queryset(queryset)

        if not filtered_quaeryset.exists():
            raise NotFound('По запросу ничего не найдено')

        return filtered_quaeryset

    class Meta:
        model = Shops
        fields = [
            'title',
            'city',
            'division',
            'type_format',
            'loc',
            'size',
            'is_active'
        ]