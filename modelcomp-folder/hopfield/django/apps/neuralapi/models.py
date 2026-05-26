from django.db import models

# Create your models here.
class HopfieldMachine(models.Model):
    name = models.TextField()
    weights = models.BinaryField()
    dims = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class HopfieldExercise(models.Model):
    machine = models.ForeignKey(HopfieldMachine, on_delete=models.CASCADE, related_name='ejercicios')
    inputs = models.JSONField(help_text="Lista de floats (flattened array)")
    result = models.JSONField(null=True, blank=True)
    is_convergent = models.BooleanField(default=False)
    epochs = models.IntegerField(default=0)
    image = models.ImageField(upload_to='hopfield/results/', null=True)