from django.urls import include, path
from unloads import views

app_name = "unloads"

unloads_urlpattern = [
    path("", views.UnloadListView.as_view(), name="unloads"),
    path(
        "<str:page_name>/", views.DataExportView.as_view(), name="data_unloads"
    ),
    path(
        "<int:pk>/delete",
        views.DeleteUnloadView.as_view(),
        name="delete_unload",
    ),
]

urlpatterns = [
    path("unloads/", include(unloads_urlpattern)),
]
