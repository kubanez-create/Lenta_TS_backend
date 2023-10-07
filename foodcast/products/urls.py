from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from .views import ForecastViewSet, ProductViewSet, ShopsViewSet, StatisticViewSet

app_name = "products"

router = DefaultRouter()
router.register(r"shops", ShopsViewSet, basename="shops")
router.register(r"product", ProductViewSet, basename="product")
router.register(r"forecast", ForecastViewSet, basename="forecast")
router.register(r"statistic", StatisticViewSet, basename="statistic")

urlpatterns = [
    re_path(r"^(?P<version>(v1|v2))/", include(router.urls)),
]
"""    re_path(
        r'^(?P<version>(v1|v2))/',
        ForecastViewSet.as_view({'get': 'excel_forecast_download'}),
        ),"""
