from MultilayerPerceptron.sigmoid_layer import SigmoidHiddenLayer, SigmoidOutputLayer
import numpy as np
import numpy.typing as npt

import matplotlib.pyplot as plt
       
class MLPerceptron:
    input_size: int
    feature_size: int

    neurons_per_layer: int
    hidden_layers: int

    layers: list[SigmoidHiddenLayer | SigmoidOutputLayer]

    error_values: list[float]

    def __init__(self, input_size: int, feature_size: int, learning_constant: float, neurons_per_layer: int, hidden_layers: int):
        self.input_size = input_size
        self.feature_size = feature_size
        self.learning_constant = learning_constant

        self.neurons_per_layer = neurons_per_layer
        self.hidden_layers = hidden_layers

        self.layers = []
        self.error_values = []

        self.initialize_perceptron()


    def initialize_perceptron(self):
        self.layers.append(SigmoidHiddenLayer(self.input_size, self.feature_size, self.learning_constant, self.neurons_per_layer))

        for _ in range(self.hidden_layers):
            self.layers.append(SigmoidHiddenLayer(self.input_size, self.neurons_per_layer, self.learning_constant, self.neurons_per_layer))

        self.layers.append(SigmoidOutputLayer(self.input_size, self.neurons_per_layer, self.learning_constant, self.input_size))


    def forward(self, inputs: npt.NDArray[np.float16]):
        output = inputs

        for layer in self.layers:
            output = layer.activation(output)

        return output

    def calculate_result(self, inputs: npt.NDArray[np.float16], expected: npt.NDArray[np.float16], max_iterations: int, threshold: float):
        for epoch in range(max_iterations):
            activaciones = [inputs]

            # 1. Propagación hacia adelante
            for layer in self.layers:
                activaciones.append(layer.activation(activaciones[-1]))
            
            result = activaciones[-1] # El resultado final de la red
            
            # 2. Verificación de convergencia (MSE)
            mse = np.mean(np.square(expected - result))
            self.error_values.append(mse)

            if epoch % 4 == 0:
                print(f"Epoch {epoch} - Promedio de pesos Capa 1: {np.mean(self.layers[0].weight)}")
                print(f"Activaciones Capa Oculta:\n{activaciones[1]}") # ¿Son todas iguales?

            if mse <= threshold:
                print(f"Convergió en epoch {epoch+1} con MSE: {mse:.8f}")
                return result

            # 3. Cálculo de deltas
            deltas = []

            output_layer: SigmoidOutputLayer = self.layers[-1]
            error_out = output_layer.calculate_error(expected, result)
            delta_out = output_layer.delta_output(error_out, result)
            deltas.append(delta_out)

            for i in range(len(self.layers) - 2, -1, -1):
                capa_actual: SigmoidHiddenLayer = self.layers[i]
                capa_siguiente: SigmoidHiddenLayer = self.layers[i+1]
                
                # El error oculto usa el delta y los pesos de la capa de adelante
                error_h = capa_actual.calculate_error(deltas[-1], capa_siguiente.weight)

                # El resultado de la activación de esta capa es activaciones[i+1]
                delta_h = capa_actual.delta_output(error_h, activaciones[i+1])
                deltas.append(delta_h)

            # 4. Actualización de Pesos (Deltas están al revés)
            deltas.reverse()

            for i, layer in enumerate(self.layers):
                layer.weight += layer.learning_constant * np.dot(activaciones[i].T, deltas[i])
                layer.bias += layer.learning_constant * np.sum(deltas[i], axis=0, keepdims=True)

        self.graphicate(is_error=True)
        raise MemoryError(f"Se alcanzó el máximo de {max_iterations} epochs sin lograr el error mínimo de {threshold}.")


    def graphicate(self, is_error: bool = False):
        fig, ax = plt.subplots()

        ax.plot([i for i in range(1, len(self.error_values)+1)], self.error_values, color=f"{'red' if is_error else 'green'}", marker='o')
        ax.set_title('')
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Error (%)')

        plt.show()


if __name__ == "__main__":
    # Contexto: [Vel_x, Vel_y, Vel_z] de 2 balones
    # El valor -3.5 indica dirección opuesta en el eje Z
    entradas = np.array([
        [4.0, 3.0, -3.5],
        [2.2, 4.1, 2.0]
    ], dtype=np.float64)

    # Valores deseados
    # [Distancia Nivel Mar, Distancia La Paz]
    expected_result = np.array([
        [35.5, 48.2], # Balón 1
        [28.0, 39.5]  # Balón 2
    ], dtype=np.float64)

    # Se normalizan los valores deseados
    expected_max = np.max(expected_result)
    expected_result = (1 / expected_max) * expected_result

    # Creamos un MLP: 3 Entradas -> 5 Neuronas Ocultas -> 2 Salidas
    # Usamos una capa oculta para captar la fricción no lineal del aire
    red = MLPerceptron(np.shape(entradas)[0], np.shape(entradas)[1], learning_constant=0.15, neurons_per_layer=5, hidden_layers=2)

    print("--- Iniciando Entrenamiento del MLP ---")
    resultado_final = red.calculate_result(entradas, expected_result, max_iterations=10000, threshold=0.007)

    print(f"\nEntradas (Velocidades):\n{entradas}")
    print(f"\nResultados Predichos (Normalizados):\n{resultado_final}")
    print(f"\nResultados Reales (Metros):\n{resultado_final * expected_max}")

    red.graphicate()
    