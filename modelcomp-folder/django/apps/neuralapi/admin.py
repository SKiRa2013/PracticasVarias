from django.contrib import admin

# Register your models here.
from apps.neuralapi.models import HopfieldMachine, HopfieldExercise

import numpy as np
import io

# Registro simple
@admin.register(HopfieldMachine)
class HopfieldMachineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display_weights', 'dims', 'created_at')
    # list_filter = ()

    readonly_fields = ('display_weights',)
    
    def display_weights(self, obj):
        if not obj.weights:
            return "No weights calculated"
        
        try:
            # Reconstruimos la matriz desde los bytes
            buffer = io.BytesIO(obj.weights)
            weights_matrix = np.load(buffer)
            
            # Formateamos para que no salga una pared de texto infinita
            # Esto mostrará solo los bordes si la matriz es muy grande
            with np.printoptions(threshold=100, precision=3, suppress=True):
                return str(weights_matrix)
        except Exception as e:
            return f"Error at decoding weights: {e}"

    # Le damos un nombre bonito a la columna en el Admin
    display_weights.short_description = "weights"

# Registro un poco más avanzado para ver más columnas
@admin.register(HopfieldExercise)
class HopfieldExerciseAdmin(admin.ModelAdmin):
    list_display = ('id', 'machine', 'is_convergent', 'epochs', 'inputs', 'result', 'image')
    # list_filter = ('is_convergent', 'machine')
