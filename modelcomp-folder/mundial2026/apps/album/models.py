from django.db import models

# Create your models here.
class Team(models.Model):
    """ Equipo """
    name = models.CharField(max_length=50, verbose_name="Nombre de equipo")
    logo = models.ImageField(upload_to='mundial2026/logos/', verbose_name="Logo (Imagen)")
    team = models.ImageField(upload_to='mundial2026/teams/', verbose_name="Equipo completo (Imagen)")
    pub_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    """ Jugador """
    team = models.ForeignKey('Team', on_delete=models.PROTECT, related_name='get_player', verbose_name="Equipo de jugador")
    first_name = models.CharField(max_length=50, verbose_name="Nombre(s)")
    last_name = models.CharField(max_length=50, verbose_name="Apellido(s)")
    photo = models.ImageField(upload_to='mundial2026/players/', verbose_name="Foto (Imagen)")
    pub_date = models.DateField(auto_now_add=True)
    height = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="Altura (m)")
    weight = models.IntegerField(verbose_name="Peso (Kg)")
    comment = models.CharField(max_length=200, blank=True, verbose_name="Descripción")

    def __str__(self):
        return self.first_name + " " + self.last_name