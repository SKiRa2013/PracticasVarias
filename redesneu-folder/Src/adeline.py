import math
import numpy as np
import numpy.typing as npt

class AdelineLayer:
    bias: npt.NDArray[np.float16]
    weight: npt.NDArray[np.float16]
    feature_size: int
    input_size: int
    neurons: int
    
    MAX_ITERATIONS: int

    learning_constant: float

    def __init__(self, input_size: int, feature_size: int, learning_constant: float, neurons: int = 1) -> None:
        self.input_size = input_size
        self.feature_size = feature_size
        self.neurons = neurons
        self.learning_constant = learning_constant

        self.MAX_ITERATIONS = 100

        self.weight = np.zeros((feature_size, neurons), dtype=np.float16)
        self.bias = np.zeros((input_size, neurons), dtype=np.float16)
        
    def calculate_result(self, inputs: npt.NDArray, threshold: float, expected_result: npt.NDArray, result: npt.NDArray) -> npt.NDArray:
        print(f"Se procede a la calibración de los pesos con respecto a los valores teóricos deseados:\n{expected_result}\n")

        epoch = 1
        mse = self.calculate_mse(expected_result, result)

        print(f"Ritmo de aprendizaje: {self.learning_constant}\nIteración 1: \nValor de LSM: {mse:.8f} vs Error mínimo: {threshold}\n")

        while mse > threshold:
            if epoch > self.MAX_ITERATIONS:
                raise MemoryError("Demasiadas iteraciones, cancelando...")
            
            epoch += 1

            print(f"Iteración {epoch}:\n")

            self.update_weight(inputs, expected_result, result)
            result = self.activation(inputs)

            print(f"Nuevos pesos:\n{self.weight}\n")
            print(f"Nuevo resultado:\n{result}\n")

            mse = self.calculate_mse(expected_result, result)

            print(f"Valor de LSM: {mse:.8f} vs Error mínimo: {threshold}\n")

        print(f"\nIteraciones finalizadas. Epoch: {epoch}")
        return result
    
    def set_weight(self, weight_list: list[float, float]) -> None:
        dim: tuple[int, int] = np.shape(weight_list)
    
        if dim[0] != self.feature_size:
            raise ValueError(f"Se esperaban {self.feature_size} parámetros por entrada, pero se obtuvieron {dim[0]}.")
    
        self.weight = np.array(weight_list, dtype=np.float16)
    
    def set_bias(self, bias_list: list[float, float]) -> None:
        dim: tuple[int, int] = np.shape(bias_list)
    
        if dim[0] != self.input_size:
            raise ValueError(f"Se esperaban {self.input_size} entradas, pero se obtuvieron {dim[0]}.")
    
        if dim[1] != self.neurons:
            raise ValueError(f"Las neuronas del sistema son {self.neurons}, pero se referencian {dim[1]}")
    
        self.bias = np.array(bias_list, dtype=np.float16)
    
    def activation(self, inputs: npt.NDArray[np.float16]) -> npt.NDArray:
        return np.dot(inputs, self.weight) + self.bias
    
    def calculate_mse(self, expected_result: npt.NDArray, result: npt.NDArray) -> float:
        if np.shape(expected_result) != np.shape(result):
            print("ay mi madre")
            print(f"{np.shape(expected_result)=} vs {np.shape(result)}")

            raise ValueError(f"Los resultados no tienen la misma dimensión")
        
        prom = np.mean(np.square(expected_result - result))
        
        if math.isinf(prom):
            raise ValueError(f"El cálculo es divergente, no se puede llegar a la respuesta.")
        
        return prom

    def update_weight(self, inputs:npt.NDArray, expected_result: npt.NDArray, result: npt.NDArray) -> None:
        self.weight = self.weight + np.dot(
            np.transpose(inputs),
            ( self.learning_constant * (expected_result - result) )
        )


if __name__ == "__main__":
    entradas = np.array([
        [4, 3, -3.5],
        [2.2, 4.1, 2]
    ], dtype=np.float16)

    expected_result = np.array([
        [1, 2],
        [3, 4]
    ], dtype=np.float16)

    capa = AdelineLayer(input_size = np.shape(entradas)[0], feature_size = np.shape(entradas)[1], learning_constant=0.01, neurons=2)
    capa.set_weight([[1, 2], [2, 0.5], [3, 2]])
    capa.set_bias([[-1, -3], [0.1, 0.2]])
    result = capa.activation(entradas)

    print(f"Batch de entradas:\n{entradas}\n")
    print(f"Pesos iniciales:\n{capa.weight}\n")
    print(f"Sesgo:\n{capa.bias}\n")
    print(f"Resultados:\n{result}\n")
    
    capa.calculate_result(entradas, 0.02, expected_result, result)
