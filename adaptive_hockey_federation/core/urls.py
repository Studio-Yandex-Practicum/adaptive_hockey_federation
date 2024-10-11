from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls", namespace="main")),
    path("", include("users.urls", namespace="users")),
    path("", include("competitions.urls", namespace="competitions")),
    path("", include("analytics.urls", namespace="analytics")),
    path("", include("unloads.urls", namespace="unloads")),
    path("auth/", include("django.contrib.auth.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "core.views.not_found"
handler403 = "core.views.forbidden"
handler500 = "core.views.internal_server_error"
