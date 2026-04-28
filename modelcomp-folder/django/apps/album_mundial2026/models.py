from django.db import models

# Create your models here.
class Team(models.Model):
    """ Equipo """
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='mundial2026/logos/')
    team = models.ImageField(upload_to='mundial2026/teams/')
    pub_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    """ Jugador """
    team = models.ForeignKey('Team', on_delete=models.PROTECT, related_name='get_player')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='mundial2026/players/')
    pub_date = models.DateField(auto_now_add=True)
    height = models.DecimalField(max_digits=3, decimal_places=2)
    weight = models.IntegerField()
    comment = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name
        