import numpy as np
import numpy.typing as npt

class Neuron:
    threshold: float
    weight: npt.NDArray[np.float16]
    input_size: int

    def __init__(self, input_size, threshold = 0):
        self.threshold = threshold
        self.input_size = input_size
        self.weight = np.zeros(input_size, dtype=np.float16)

    def set_weight(self, weight_list: list[float]):
        dim: int = np.shape(weight_list)[0]
        
        if dim != self.input_size:
            raise ValueError(f"Se esperaban {self.input_size} pesos, pero se obtuvieron {dim}.")

        self.weight = np.array(weight_list, dtype=np.float16)

    def activation(self, inputs: npt.NDArray[np.float16]) -> npt.NDArray:
        return np.dot(inputs, self.weight)

    def output_sign(self, result: float):
        return -1 if result < 0 else 1


if __name__ == "__main__":
    entrada = np.array([4, 3, -3.5], dtype=np.float16)

    neurona = Neuron(input_size=np.shape(entrada)[-1], threshold=15)
    neurona.set_weight([1, 2, 3])
    
    result = neurona.activation(entrada)

    print(f"El umbral de la neurona es {neurona.threshold}")
    print(f"La neurona posee {neurona.input_size} input_size")
    print(f"Los pesos de la neurona es {neurona.weight}")

    print(f"La función de activación entre {entrada} y {neurona.weight} es {result}")

    print(f"El resultado final al aplicar la función signo es {neurona.output_sign(result)}\n")

    print("=" * 100)
    print()

    neurona2 = Neuron(input_size=np.shape(entrada)[-1], threshold=15)
    neurona2.set_weight([1, 2, 2.75])

    result2 = neurona2.activation(entrada)

    print(f"El umbral de la neurona es {neurona2.threshold}")
    print(f"La neurona posee {neurona2.input_size} input_size")
    print(f"Los pesos de la neurona es {neurona2.weight}")

    print(f"La función de activación entre {entrada} y {neurona2.weight} es {result2}")

    print(f"El resultado final al aplicar la función signo es {neurona.output_sign(result2)}")