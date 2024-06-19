from django.urls import path
from video_api.views import VideoRecognitionView


urlpatterns = [
    path("video_recognition_test/<int:pk>/", VideoRecognitionView.as_view()),
]
