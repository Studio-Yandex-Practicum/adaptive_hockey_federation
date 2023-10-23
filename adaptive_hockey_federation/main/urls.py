from django.urls import path

from . import views

app_name = 'main'


urlpatterns = [
    path('users/', views.users, name='users'),
    path('teams/<int:id>/', views.teams_id, name='teams_id'),
    path('teams/', views.teams, name='teams'),
    path(
        'competitions/<int:id>/',
        views.competitions_id,
        name='competitions_id',
    ),
    path('competitions/', views.competitions, name='competitions'),
    path('analytics/', views.analytics, name='analytics'),
    path('unloads/', views.unloads, name='unloads'),
]
