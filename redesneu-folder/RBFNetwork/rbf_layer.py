from MultilayerPerceptron.sigmoid_layer import SigmoidLayer, SigmoidOutputLayer

import numpy as np
import numpy.typing as npt

class RBFLayer(SigmoidLayer):
    sigma: float

    def __init__(self, input_size: int, feature_size: int, neurons: int):
        super().__init__(input_size, feature_size, 0, neurons)
        self.weight = np.random.uniform(-1, 1, (feature_size, neurons)).astype(np.float16)

    def calculate_sigma(self):
        """
        Calcula sigma = d_max / sqrt(2 * n_neuronas)
        """
        # Calculamos la matriz de distancias entre todos los centroides
        # weight.T tiene dimensiones (neuronas, features)
        c = self.weight.T
        
        # Distancia euclidiana entre cada par de centros
        # (usamos el truco de la norma para obtener d_max)
        dists = np.linalg.norm(c[:, np.newaxis, :] - c[np.newaxis, :, :], axis=2)
        d_max = np.max(dists)
        
        self.sigma = d_max / np.sqrt(2 * self.neurons)
        
        # Evitar división por cero si d_max es 0 o se aproxima
        if -1e-06 < self.sigma < 1e-06:
            self.sigma = 1.0

    def activation(self, inputs: npt.NDArray[np.float16]) -> npt.NDArray[np.float16]:
        # En RBF, calculamos la distancia euclidiana: ||x - c||^2
        # Usamos broadcasting para restar cada entrada de cada centro
        dist = np.linalg.norm(inputs[:, np.newaxis, :] - self.weight.T, axis=2)
        return np.exp(-(np.square(dist)) / (2 * (self.sigma**2)))

    def delta_output(self, error, result):
        return np.zeros_like(result)
    
    def update_centers(self, inputs: npt.NDArray[np.float16]) -> bool:
        """
        Una iteración estilo K-Means para mover los centros hacia 
        los grupos de datos reales. Devuelve True si los centros cambiaron, False si se estabilizaron.
        """
        old_centers = np.copy(self.weight)
        
        # 1. Encontrar a qué centro pertenece cada dato (el más cercano)
        dist = np.linalg.norm(inputs[:, np.newaxis, :] - self.weight.T, axis=2)
        closest_centers = np.argmin(dist, axis=1)

        # 2. Mover cada centro al promedio de los puntos que le fueron asignados
        for i in range(self.neurons):
            points_in_cluster = inputs[closest_centers == i]
            if len(points_in_cluster) > 0:
                # Actualización suave del centro
                self.weight[:, i] = np.mean(points_in_cluster, axis=0)

        # Verificamos si hubo cambios significativos
        # Usamos atol (absolute tolerance) por precisión de punto flotante
        return not np.allclose(old_centers, self.weight, atol=1e-6)
        

class RBFOutputLayer(SigmoidOutputLayer):
    def __init__(self, input_size, feature_size, neurons):
        # La constante de aprendizaje no se usa aquí porque el cálculo es directo
        super().__init__(input_size, feature_size, 0, neurons)

    def solve_pseudo_inverse(self, hidden_activations: npt.NDArray, expected_output: npt.NDArray):
        """
        Aplica la fórmula: W = pinv(G) * Y
        hidden_activations (G): Salida de la capa RBF oculta
        expected_output (Y): Valores deseados
        """
        # Calculamos la pseudoinversa de la matriz de activaciones
        pinv_g = np.linalg.pinv(hidden_activations)
        
        # Los nuevos pesos son el producto de la pinv y la salida esperada
        # Nota: En este enfoque, el bias suele incluirse como una columna de 1s en G
        self.weight = np.dot(pinv_g, expected_output).astype(np.float16)
        
    def activation(self, inputs: npt.NDArray[np.float16]) -> npt.NDArray[np.float16]:
        # La salida en una RBF clásica con pseudoinversa es LINEAL
        return np.dot(inputs, self.weight)
    