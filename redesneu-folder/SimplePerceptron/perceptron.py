import numpy as np
import numpy.typing as npt

class PerceptronLayer:
    bias: npt.NDArray[np.float16]
    weight: npt.NDArray[np.float16]
    feature_size: int
    input_size: int
    neurons: int

    def __init__(self, input_size, feature_size, neurons = 1):
        self.input_size = input_size
        self.feature_size = feature_size
        self.neurons = neurons
        self.weight = np.zeros((feature_size, neurons), dtype=np.float16)
        self.bias = np.zeros((input_size, neurons), dtype=np.float16)
    
    def set_weight(self, weight_list: list[float, float]):
        dim: tuple[int, int] = np.shape(weight_list)
    
        if dim[0] != self.feature_size:
            raise ValueError(f"Se esperaban {self.feature_size} parámetros por entrada, pero se obtuvieron {dim[0]}.")
    
        self.weight = np.array(weight_list, dtype=np.float16)
    
    def set_bias(self, bias_list: list[float, float]):
        dim: tuple[int, int] = np.shape(bias_list)
    
        if dim[0] != self.input_size:
            raise ValueError(f"Se esperaban {self.input_size} entradas, pero se obtuvieron {dim[0]}.")
    
        if dim[1] != self.neurons:
            raise ValueError(f"Las neuronas del sistema son {self.neurons}, pero se referencian {dim[1]}")
    
        self.bias = np.array(bias_list, dtype=np.float16)
    
    def activation(self, inputs: npt.NDArray[np.float16]) -> npt.NDArray:
        return np.dot(inputs, self.weight) + self.bias
    
    def output_sign(self, result: float):
        return -1 if result < 0 else 1
    

if __name__ == "__main__":
    entradas = np.array([
    [4, 3, -3.5],
    [2.2, 4.1, 2]
    ], dtype=np.float16)

    capa = PerceptronLayer(input_size = np.shape(entradas)[0], feature_size = np.shape(entradas)[1], neurons=2)
    capa.set_weight([[1, 2], [2, 0.5], [3, 2]])
    # capa.set_bias()
    result = capa.activation(entradas)

    capa2 = PerceptronLayer(input_size = np.shape(entradas)[0], feature_size = np.shape(entradas)[1], neurons=2)
    capa2.set_weight([[1, 2], [2, 0.5], [3, 2]])
    capa2.set_bias([[-10, -1], [8, -0.5]])
    result2 = capa2.activation(entradas)

    print(f"Se usó el siguiente batch de entradas: {entradas}\n")
    print(f"En ambos ejemplos se usaron estos pesos: {capa.weight}\n")
    print(f"El primer ejemplo no tiene sesgo, el segundo tiene estos valores: {capa2.bias}\n")
    print(f"Los resultados son:\nPara el primer ejemplo: {result}\nPara el segundo ejemplo: {result2}")
    print(f"Ejemplo con capa neuronal sin sesgo.")

    for e in range(np.shape(entradas)[0]):
        for n in range(capa.neurons):
            print(f"Para la entrada {e+1}, la neurona {n+1} con resultado {result[e][n]} entrega el output_sign = {capa.output_sign(result[e][n])}")
            print(f"Ejemplo con capa neuronal con sesgo.")

    for e in range(np.shape(entradas)[0]):
            for n in range(capa2.neurons):
                print(f"Para la entrada {e+1}, la neurona {n+1} con resultado {result2[e][n]} entrega el output_sign = {capa.output_sign(result2[e][n])}")