from analytics import views
from django.urls import include, path

app_name = "analytics"

analytics_urlpatterns = [
    path("", views.AnalyticsListView.as_view(), name="analytics"),
]

urlpatterns = [
    path('analytics/', include(analytics_urlpatterns))
]
