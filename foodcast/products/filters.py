import django_filters
from django.forms.fields import MultipleChoiceField
from django_filters import FilterSet
from rest_framework.exceptions import NotFound

from .models import Forecast, Shops


class ShopFilter(FilterSet):
    title = django_filters.CharFilter(lookup_expr='exact')
    city = django_filters.CharFilter(lookup_expr='exact')
    division = django_filters.CharFilter(lookup_expr='exact')
    type_format = django_filters.CharFilter(lookup_expr='exact')
    loc = django_filters.CharFilter(lookup_expr='exact')
    size = django_filters.CharFilter(lookup_expr='exact')
    is_active = django_filters.CharFilter(lookup_expr='exact')

    def filter_queryset(self, queryset):
        filtered_queryset = super().filter_queryset(queryset)

        if not filtered_queryset.exists():
            raise NotFound('По запросу ничего не найдено')

        return filtered_queryset

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

class MultipleField(MultipleChoiceField):
    def valid_value(self, value):
        return True


class MultipleFilter(django_filters.MultipleChoiceFilter):
    field_class = MultipleField


class SalesFilter(FilterSet):
    store = MultipleFilter(field_name="store")
    group = MultipleFilter(field_name="SKU__group")
    category = MultipleFilter(field_name="SKU__category")
    subcategory = MultipleFilter(field_name="SKU__subcategory")


class ForecastFilter(FilterSet):
    store = MultipleFilter(field_name="store")
    group = MultipleFilter(field_name="sku__group")
    category = MultipleFilter(field_name="sku__category")
    subcategory = MultipleFilter(field_name="sku__subcategory")
