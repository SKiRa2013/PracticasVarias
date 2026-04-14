import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt

from redesneu.perceptron import PerceptronLayer

class Hopfield(PerceptronLayer):   
    def __init__(self, inputs: npt.NDArray[np.float16]):
        super().__init__(input_size=inputs.shape[0], feature_size=inputs.shape[1])

        self.neurons = self.feature_size
        self.set_weight(inputs)

    def set_weight(self, inputs: npt.NDArray):
        self.weight = np.dot(inputs.T, inputs)
        np.fill_diagonal(self.weight, 0)

    def activation(self, inputs: npt.NDArray) -> npt.NDArray[np.float16]:
        return np.sign(inputs)
    
    def iterate(self, inputs: npt.NDArray[np.float16], max_iterations: int) -> tuple:
        if inputs.ndim == 1:
            inputs = inputs.reshape(1, -1)
        
        aux_inputs: list[np.float16] = list(enumerate(list(np.copy(inputs))))
        result: npt.NDArray[np.float16] = np.zeros((inputs.shape[0], self.feature_size), dtype=np.float16)

        print(f"{inputs.shape=}")
        print(f"{result.shape=}")

        for epoch in range(1, max_iterations + 1):
            if len(aux_inputs) == 0:
                print(f"¡CONVERGENCIA! Epochs: {epoch}. Matriz: {result}")
                return (result, epoch)
            
            pending: list[np.float16] = []
        
            for idx, row in aux_inputs:
                output = self.activation(np.dot(row, self.weight))

                print(f"{output.shape = }")
                print(f"{row.shape = }")

                if np.array_equal(output, row):
                    result[idx] = output
                else:
                    pending.append((idx, output))

            aux_inputs = pending
        else:
            raise RuntimeError(f"Se ha alcanzado el máximo de {epoch} epochs. No hay convergencia.")


def graphicate(original, noisy, recovered, shape=(5, 5)):
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))
    
    axs[0].imshow(original.reshape(shape), cmap='gray_r')
    axs[0].set_title('Patrón Original (Z)')
    axs[0].axis('off')

    axs[1].imshow(noisy.reshape(shape), cmap='gray_r')
    axs[1].set_title('Entrada con Ruido')
    axs[1].axis('off')

    axs[2].imshow(recovered.reshape(shape), cmap='gray_r')
    axs[2].set_title('Resultado Red Hopfield')
    axs[2].axis('off')

    plt.show()

if __name__ == "__main__":
    # Letra 'Z'
    char_z = np.array([
        [ 1,  1,  1,  1,  1],
        [-1, -1, -1,  1, -1],
        [-1, -1,  1, -1, -1],
        [-1,  1, -1, -1, -1],
        [ 1,  1,  1,  1,  1]
    ], dtype=np.float16).flatten()

    # Letra 'N'
    char_n = np.array([
        [ 1, -1, -1, -1,  1],
        [ 1,  1, -1, -1,  1],
        [ 1, -1,  1, -1,  1],
        [ 1, -1, -1,  1,  1],
        [ 1, -1, -1, -1,  1]
    ], dtype=np.float16).flatten()
    
    # Patrón de prueba con ruido basado en la 'Z'
    test_input = np.copy(char_z)

    noise_indices = np.random.choice(25, 5, replace=False)
    test_input[noise_indices] *= -1 
    print(f"Patrón de prueba creado invirtiendo {len(noise_indices)} píxeles de la 'Z'.")

    # Red de Hopfield, prueba con caracter Z
    entrada = []
    entrada.append(char_z)
    entrada.append(char_n)
    entrada = np.array(entrada)

    hop = Hopfield(entrada)
    result = hop.iterate(char_z, max_iterations=20)

    # Original, ruido, hopfield
    graphicate(char_z, test_input, result)
