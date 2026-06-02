from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy, get_resolver
from django.urls.resolvers import URLResolver, URLPattern

from apps.album.models import Player, Team

# Create your views here.
class IndexView(TemplateView):
    # Django buscará automáticamente este archivo en tus carpetas de templates
    template_name = 'album/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resolver = get_resolver()
        endpoints = []

        # Función interna recursiva para procesar las rutas internas e inclusiones
        def procesar_rutas(patterns, prefijo=''):
            for pattern in patterns:
                # Si es un include(), es un URLResolver y contiene más rutas dentro
                if isinstance(pattern, URLResolver):
                    # Limpiamos el formato del patrón para quitar expresiones regulares si las hay
                    nuevo_prefijo = prefijo + str(pattern.pattern)
                    procesar_rutas(pattern.url_patterns, prefijo=nuevo_prefijo)
                
                # Si es una ruta final (URLPattern), la guardamos
                elif isinstance(pattern, URLPattern):
                    # Evitamos meter la propia vista del índice para no crear un bucle infinito
                    if pattern.name != 'index':
                        ruta_completa = prefijo + str(pattern.pattern)
                        
                        # Limpieza básica para que se vea estético en las etiquetas <a>
                        ruta_limpia = '/' + ruta_completa.replace('^', '').replace('$', '')
                        
                        if ruta_limpia.startswith('/album') and (ruta_limpia.endswith('teams/') or ruta_limpia.endswith('players/')):
                            endpoints.append({
                                'url': ruta_limpia,
                                'nombre': pattern.name or ruta_limpia
                            })

        # Iniciamos el procesamiento con los patrones raíz del proyecto
        procesar_rutas(resolver.url_patterns)
        
        context['endpoints'] = endpoints
        return context
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
