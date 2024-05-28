from django.urls import path

from .views import (
    receiving_data_game,
    receiving_data_player,
    send_data_game,
    send_data_player,
)

urlpatterns = [
    path('send_player/', send_data_player, name='send_data_player'),
    path('get_player/', receiving_data_player, name='receiving_data_player'),
    path('get_player/<int:pk>/', receiving_data_player,
         name='receiving_data_player_by_pk'),
    path('send_game/', send_data_game, name='send_data_game'),
    path('get_game/', receiving_data_game, name='receiving_data_game'),
    path('get_game/<int:pk>/', receiving_data_game,
         name='receiving_data_game_by_pk'),
]
