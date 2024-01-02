from django.urls import path
from main import views

app_name = 'main'


urlpatterns = [
    path('', views.main, name='main'),
    path('players/', views.players, name='players'),
    path('teams/<int:id>/', views.TeamIdView.as_view(), name='teams_id'),
    path('teams/', views.TeamListView.as_view(), name='teams'),
    path(
        'competitions/<int:id>/',
        views.competitions_id,
        name='competitions_id',
    ),
    path('competitions/', views.competitions, name='competitions'),
    path('analytics/', views.analytics, name='analytics'),
    path('unloads/', views.unloads, name='unloads'),
]
