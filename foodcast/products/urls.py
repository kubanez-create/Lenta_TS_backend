from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from .views import ForecastViewSet, ProductViewSet, ShopsViewSet, StatisticView

app_name = "products"

router = DefaultRouter()
router.register(r"shops", ShopsViewSet, basename="shops")
router.register(r"product", ProductViewSet, basename="product")
router.register(r"forecast", ForecastViewSet, basename="forecast")

urlpatterns = [
    re_path(r"^(?P<version>(v1|v2))/", include(router.urls)),
    re_path(
        r"^(?P<version>(v1|v2))/statistics",
        StatisticView.as_view(),
        name="statistics"
    ),
]
