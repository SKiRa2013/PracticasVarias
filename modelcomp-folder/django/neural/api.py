from redesneu.hopfield import Hopfield
from neural.models import HopfieldMachine, HopfieldExercise
from neural.serializers import MachineSerializer, ExerciseSerializer
from rest_framework import viewsets, permissions

from django.core.files.base import ContentFile

import io
import numpy as np
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def graphicate(machine, inputs, result, epoch) -> io.BytesIO:
    n = int(math.sqrt(machine.dims))

    # 2. Aseguramos que los arrays estén aplanados para guardarlos,
    # pero les damos forma (reshape) solo para el gráfico
    result_flat = result.flatten()
    inputs_flat = inputs.flatten()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Usamos la 'n' calculada dinámicamente
    ax1.imshow(inputs_flat.reshape(n, n), cmap='gray')
    ax1.set_title(f"Entrada ({machine.dims} neuronas)")

    ax2.imshow(result_flat.reshape(n, n), cmap='gray')
    ax2.set_title(f"Resultado (Época: {epoch})")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig) # Liberar memoria
    buf.seek(0)

    return buf

class MachineViewSet(viewsets.ModelViewSet):
    queryset = HopfieldMachine.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = MachineSerializer

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = HopfieldExercise.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ExerciseSerializer

    def perform_create(self, serializer):
        machine = serializer.validated_data['machine']
        weights_buffer = io.BytesIO(machine.weights)
        weights = np.load(weights_buffer)

        aux_machine = Hopfield(np.zeros((weights.shape[0], weights.shape[1]), dtype=np.float16))
        aux_machine.weight = weights

        inputs = np.array(serializer.validated_data['inputs'], dtype=np.float16)
        
        try:
            result, epoch = aux_machine.iterate(inputs=inputs, max_iterations=30)
            convergence = True
        except RuntimeError:
            result = []
            convergence = False
            epoch = 30

        img_buffer = graphicate(machine, inputs, result, epoch)

        instance = serializer.save(
            result=result.tolist(),
            is_convergent=convergence,
            epochs=epoch,
        )

        instance.image.save(content=ContentFile(img_buffer.read()), name=f"ejercicio_{machine}_{instance.id}.png", save=True)
