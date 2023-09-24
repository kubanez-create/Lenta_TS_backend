from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

app_name = 'products'

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    re_path(
        r'^(?P<version>(v1))/',
        include(router.urls)
    ),
]
