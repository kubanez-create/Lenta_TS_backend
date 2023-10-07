from django.contrib import admin
from django.urls import include, path, re_path
from djoser.views import TokenCreateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from users.views import CustomTokenDestroyView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("products.urls", namespace="products")),
    path("api/", include("core.urls", namespace="core")),
    re_path(
        r"^api/(?P<version>(v1|v2))/auth/token/login/?$",
        TokenCreateView.as_view(),
        name="login",
    ),
    re_path(
        r"^api/(?P<version>(v1|v2))/auth/token/logout/?$",
        CustomTokenDestroyView.as_view(),
        name="logout",
    ),
]


schema_view = get_schema_view(
    openapi.Info(
        title="Lenta hackathon API",
        default_version="v1",
        description="Документация для бэкенд приложения.",
        # terms_of_service="URL страницы с пользовательским соглашением",
        contact=openapi.Contact(email="kubanez74@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc"
    ),
]
