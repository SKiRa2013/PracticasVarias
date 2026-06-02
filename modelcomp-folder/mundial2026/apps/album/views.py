from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.album.models import Player, Team

# Create your views here.

# ===================================================
#                       EQUIPOS
# ===================================================

class TeamCreateView(CreateView):
    model = Team
    fields = ['name', 'logo', 'team']
    template_name = 'album/team_form.html'
    success_url = reverse_lazy('team_list')

class TeamListView(ListView):
    model = Team
    template_name = 'album/team_list.html'

class TeamUpdateView(UpdateView):
    model = Team
    fields = ['name', 'logo', 'team']
    template_name = 'album/team_form.html'
    success_url = reverse_lazy('team_list')

class TeamDeleteView(DeleteView):
    model = Team
    template_name = 'album/team_delete.html' # Debemos crear este
    success_url = reverse_lazy('team_list')

# ===================================================
#                      JUGADORES
# ===================================================

class PlayerCreateView(CreateView):
    model = Player
    # Incluimos todos los campos, Django creará el select del equipo automáticamente
    fields = ['team', 'first_name', 'last_name', 'photo', 'height', 'weight', 'comment']
    template_name = 'album/player_form.html'
    success_url = reverse_lazy('player_list')

class PlayerListView(ListView):
    model = Player
    template_name = 'album/player_list.html'

class PlayerUpdateView(UpdateView):
    model = Player
    fields = ['team', 'first_name', 'last_name', 'photo', 'height', 'weight', 'comment']
    template_name = 'album/player_form.html'
    success_url = reverse_lazy('player_list')

class PlayerDeleteView(DeleteView):
    model = Player
    template_name = 'album/player_delete.html'
    success_url = reverse_lazy('player_list')
