from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('auth/', include('users.urls', namespace='users')),
    path("__debug__/", include("debug_toolbar.urls")),
]
