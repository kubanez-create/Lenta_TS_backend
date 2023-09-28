from django.contrib import admin
from django.urls import path, include, re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls', namespace='products')),
    re_path(
            r'^api/(?P<version>(v1|v2))/',
            include('djoser.urls')
    ),
    re_path(
            r'^api/(?P<version>(v1|v2))/',
            include('djoser.urls.authtoken')
    )
]

