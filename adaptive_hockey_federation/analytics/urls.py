from django.urls import include, path

from analytics import views

app_name = "analytics"

analytics_urlpatterns = [
    path("", views.AnalyticsListView.as_view(), name="analytics"),
]

urlpatterns = [
    path("analytics/", include(analytics_urlpatterns)),
]
