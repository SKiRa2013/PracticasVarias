from django.contrib import admin
from django import forms

# Register your models here.
from apps.neuralapi.models import HopfieldMachine, HopfieldExercise

import numpy as np
import io

class HopfieldMachineAdminForm(forms.ModelForm):
    training_data = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Ej: [[1.0, 1.0], [-1.0, 1.0]]'
        }),
        required=True,
        label="Datos de Entrenamiento",
        help_text="Pega aquí tu matriz de datos de entrenamiento (usa np.flatten)"
    )

    class Meta:
        model = HopfieldMachine
        fields = '__all__'

class HopfieldExerciseAdminForm(forms.ModelForm):
    input_data = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Ej: [[1.0, 1.0], [-1.0, 1.0]]'
        }),
        required=True,
        label="Datos de Entrada",
        help_text="Pega aquí tu matriz de datos de entrada (usa np.flatten)"
    )

    class Meta:
        model = HopfieldExercise
        fields = '__all__'

@admin.register(HopfieldMachine)
class HopfieldMachineAdmin(admin.ModelAdmin):
    form = HopfieldMachineAdminForm
    
    list_display = ('id', 'name', 'display_weights', 'dims', 'created_at')
    # list_filter = ()
    fields = ('name', 'training_data')

    readonly_fields = ('display_weights', 'dims', 'created_at', )
    
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


@admin.register(HopfieldExercise)
class HopfieldExerciseAdmin(admin.ModelAdmin):
    form = HopfieldExerciseAdminForm

    list_display = ('id', 'machine', 'is_convergent', 'epochs', 'inputs', 'result', 'image')
    # list_filter = ('is_convergent', 'machine')

    fields = ('machine', 'input_data')

    readonly_fields = ('is_convergent', 'epochs', 'result', 'image')
