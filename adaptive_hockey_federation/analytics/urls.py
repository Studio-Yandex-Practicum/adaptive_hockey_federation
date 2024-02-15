from analytics import views
from django.urls import path

app_name = "analytics"

urlpatterns = [
    path("analytics/", views.analytics, name="analytics"),
]
