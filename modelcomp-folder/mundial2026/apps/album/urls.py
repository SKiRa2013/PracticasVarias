from apps.album.views import (
    TeamCreateView, TeamListView, TeamUpdateView, TeamDeleteView, 
    PlayerCreateView, PlayerListView, PlayerUpdateView, PlayerDeleteView
)

from django.urls import path

urlpatterns = [
    path('teams/create/', TeamCreateView.as_view(), name='team_create'),
    path('teams/', TeamListView.as_view(), name='team_list'),
    path('teams/<int:pk>/edit/', TeamUpdateView.as_view(), name='team_edit'),
    path('teams/<int:pk>/delete/', TeamDeleteView.as_view(), name='team_delete'),

    path('players/create/', PlayerCreateView.as_view(), name='player_create'),
    path('players/', PlayerListView.as_view(), name='player_list'),
    path('players/<int:pk>/edit/', PlayerUpdateView.as_view(), name='player_edit'),
    path('players/<int:pk>/delete/', PlayerDeleteView.as_view(), name='player_delete'),
    
]