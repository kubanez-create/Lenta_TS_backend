from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, ShopsViewSet

app_name = 'products'

router = DefaultRouter()
router.register(r'shops', ShopsViewSet, basename='shops')
router.register(r'product', ProductViewSet, basename='product')

urlpatterns = [
    re_path(
        r'^(?P<version>(v1|v2))/',
        include(router.urls)
    ),
]
