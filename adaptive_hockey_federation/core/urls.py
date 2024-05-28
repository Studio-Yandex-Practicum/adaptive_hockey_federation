from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version="v1",
        description="API для управления данными игроков и игр",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("video_api.urls")),
    path("api/docs/", schema_view.with_ui(
        "swagger",
        cache_timeout=0),
        name="schema-swagger-ui"),
    path("", include("main.urls", namespace="main")),
    path("", include("users.urls", namespace="users")),
    path("", include("competitions.urls", namespace="competitions")),
    path("", include("analytics.urls", namespace="analytics")),
    path("", include("unloads.urls", namespace="unloads")),
    path("", include("games.urls", namespace="games")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("auth/", include("django.contrib.auth.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "core.views.not_found"
handler403 = "core.views.forbidden"
handler500 = "core.views.internal_server_error"
