from SimplePerceptron.neuron import Neuron
import numpy as np

class EjercicioPercep:
    def __init__(self):
        self.entrada = np.array([7, 4, 1, 2], dtype=np.float16)
        self.neuron = Neuron(np.shape(self.entrada)[-1])
        self.neuron.set_weight([-3, 1, 1, 3])
        self.result = self.neuron.activation(self.entrada)
        self.output = self.neuron.output_sign(self.result)

if __name__ == "__main__":
    ejercicio = EjercicioPercep()
    print(f"Entrada: {ejercicio.entrada}")
    print(f"Pesos: {ejercicio.neuron.weight}")
    print(f"Valor de función de activación: {ejercicio.result}")
    print(f"\nOutput: {ejercicio.output}")