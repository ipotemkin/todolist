from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

from todolist.settings import NO_FRONT
from todolist.views import health_check

schema_view = get_schema_view(
    openapi.Info(
        title="Todolist API",
        default_version="v1",
        description="API description",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("oauth/", include("social_django.urls", namespace="social")),
    path("core/", include("core.urls")),
    path("goals/", include("goals.urls")),
    path("health/", health_check),  # namespace='health_check'),
    path("bot/", include("bot.urls", namespace="bot")),
    re_path(
        "" if NO_FRONT else r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
