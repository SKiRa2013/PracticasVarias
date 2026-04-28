from django.shortcuts import render
from django.views.generic import ListView

from apps.album_mundial2026.models import Player, Team

# Create your views here.
class TeamListView(ListView):
    model = Team

class PlayerListView(ListView):
    model = Player
    