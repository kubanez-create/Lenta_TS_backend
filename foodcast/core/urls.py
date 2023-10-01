from django.urls import re_path

from .views import SalesView

app_name = 'core'

urlpatterns = [
    re_path(
        r'^(?P<version>(v1|v2))/sales/',
        SalesView.as_view(),
        name="sales"
    ),
]