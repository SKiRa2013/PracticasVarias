import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt

from SimplePerceptron.perceptron import PerceptronLayer

class Kohonen(PerceptronLayer):
    neurons: int
    learning_constant: float
    vicinity_factor: float

    centroid_coords: npt.NDArray[np.float16]
    
    def __init__(self, inputs: npt.NDArray[np.float16], input_dim: tuple[int], neurons: int, learning_constant: float, vicinity_factor: float):
        super().__init__(input_size=inputs.shape[0], feature_size=inputs.shape[1])
        self.neurons = neurons

        self.centroid_coords = np.array([ (r, c) for r in range(input_dim[0]) for c in range(input_dim[1]) ])
        self.weight = np.random.uniform(-0.5, 0.5, (self.neurons, self.feature_size)).astype(np.float16)

        self.learning_constant = learning_constant
        self.vicinity_factor = vicinity_factor


    def euclidean_distance(self, matrix_a: npt.NDArray[np.float16], matrix_b: npt.ArrayLike[np.float16]) -> float:
        return np.linalg.norm(matrix_a - matrix_b, axis=1)

    def manhattan_distance(self, pos_a: npt.NDArray[np.intp], pos_b: npt.NDArray[np.intp]) -> float:
        return np.sum(np.abs(pos_a - pos_b), axis=1)

    def vicinity_function(self, selected_idx: tuple[int]) -> npt.NDArray:
        selected_coords = self.centroid_coords[selected_idx]
        
        distances = self.manhattan_distance(selected_coords, self.centroid_coords)        
        exponent = distances / (2 * self.vicinity_factor)
        
        return np.exp(-exponent)


    def calculate_centroids(self, inputs: npt.NDArray[np.float16], max_iterations: int) -> npt.NDArray[np.float16]:
        for epoch in range(1, max_iterations + 1):
            selected_centroids = []

            for data in inputs:
                min_centroid_idx = np.argmin(self.euclidean_distance(self.weight, data))
                influence = self.vicinity_function(min_centroid_idx)

            if np.array_equal(self.weight, selected_centroids):
                print(f"ITERACIÓN FINALIZADA. Epoch: {epoch}")
                self.graphicate()
                return [1]

            self.weight += self.learning_constant * influence[:, np.newaxis] * (data - self.weight)