from apps.album_mundial2026.views import TeamListView, PlayerListView
from django.urls import path

urlpatterns = [
    path('album/teams', TeamListView.as_view(), name='teams'),
    path('album/players', PlayerListView.as_view(), name='players'),
]
