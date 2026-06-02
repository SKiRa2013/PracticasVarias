import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
import itertools
from PIL import Image

from SimplePerceptron.perceptron import PerceptronLayer

class Kohonen(PerceptronLayer):
    neurons: int
    learning_constant: float
    vicinity_factor: float

    centroid_coords: npt.NDArray[np.float16]
    input_matrix: npt.NDArray[np.float16]
    
    def __init__(self, inputs: npt.NDArray[np.float16], space_dimension: int, neurons_per_dim: int, learning_constant: float, vicinity_factor: float):
        if inputs.ndim == 1:
            inputs = inputs.reshape(1, -1)
                
        self.input_matrix = inputs
        
        print(f"{self.input_matrix = }")
        
        super().__init__(input_size=self.input_matrix.shape[0], feature_size=self.input_matrix.shape[1])
        self.neurons = neurons_per_dim ** space_dimension

        self.centroid_coords = np.array(list(itertools.product(range(neurons_per_dim), repeat=space_dimension)))
        self.weight = np.random.uniform(0, 1, (self.neurons, self.feature_size)).astype(np.float16)

        self.learning_constant = learning_constant
        self.vicinity_factor = vicinity_factor


    def euclidean_distance(self, matrix_a: npt.NDArray[np.float16], matrix_b: npt.NDArray[np.float16]) -> float:
        return np.linalg.norm(matrix_a - matrix_b, axis=1)

    def manhattan_distance(self, pos_a: npt.NDArray[np.intp], pos_b: npt.NDArray[np.intp]) -> float:
        return np.sum(np.abs(pos_a - pos_b), axis=1)

    def vicinity_function(self, selected_idx: tuple[int]) -> npt.NDArray:
        selected_coords = self.centroid_coords[selected_idx]
        
        distances = self.manhattan_distance(selected_coords, self.centroid_coords)        
        exponent = distances / (2 * self.vicinity_factor)
        
        return np.exp(-exponent)

    def graphicate(self, img_size: tuple[int], canales):
        rows, cols = img_size
    #    fig, axes = plt.subplots(rows, cols, figsize=(12, 12))
        
        # 1. Determinar la geometría de la rejilla de neuronas
        # Si tu mapa es 2D, la raíz cuadrada de self.neurons nos da el lado
        side = int(np.sqrt(self.neurons))
        rows, cols = side, side 
        
        # Si la raíz no es exacta (ej. 20 neuronas), ajustamos
        if rows * cols < self.neurons:
            rows += 1

        fig, axes = plt.subplots(rows, cols, figsize=(12, 12))
        
        # Aplanamos los ejes para iterar sin errores de índice [r, c]
        axes_flat = axes.flatten()

        for i in range(self.neurons):
            ax = axes_flat[i]
            
            try:
                # Reconstrucción RGB: (alto, ancho, 3)
                # Usamos img_size[1] para filas y img_size[0] para columnas
                imagen_neurona = self.weight[i].reshape((img_size[1], img_size[0], canales))
                
                # Clipping para asegurar que los colores sean válidos [0, 1]
                imagen_visual = np.clip(imagen_neurona.astype(np.float32), 0, 1)
                
                ax.imshow(imagen_visual)
            except Exception as e:
                # Si sobran subplots (ej. rejilla 5x5 para 20 neuronas), 
                # las dejamos en blanco
                pass
                
            ax.axis('off')

        # Limpiamos subplots vacíos si los hay
        for j in range(i + 1, len(axes_flat)):
            axes_flat[j].axis('off')

        plt.subplots_adjust(wspace=0.02, hspace=0.02)
        plt.suptitle("Mapa de Kohonen: Reconstrucción de Pesos")
        plt.show()
    
    def calculate_centroids(self, max_iterations: int) -> None:
        for epoch in range(1, max_iterations + 1):
            old_weight = np.copy(self.weight)
           
            for data in self.input_matrix:
                min_centroid_idx = np.argmin(self.euclidean_distance(self.weight, data))
                influence = self.vicinity_function(min_centroid_idx)
                self.weight += self.learning_constant * influence[:, np.newaxis] * (data - self.weight)
        
            if np.allclose(self.weight, old_weight, atol=1e-4):
                print(f"ITERACIÓN FINALIZADA. Epoch: {epoch}")
                return
                
        print(f"Iteración finalizada. Se han completado la cantidad máxima de epochs ({max_iterations})")
        return        
                
                
if __name__ == "__main__":
    personajes = {
        "doomguy": "doomguy.png",
        "max": "maxdamage.png",
        "duke": "dukenukem.png"
    }
    
    imagenes_norm = {}
    size_comun = (52, 52)

    for clave, nombre in personajes.items():
        try:
            img = Image.open(f".media/{nombre}").convert('RGB').resize(size_comun)
            assert(img.size[0] == size_comun[0] and img.size[1] == size_comun[1])
        except FileNotFoundError as e:
            print(f"No se encontró {nombre}, error {e}, creando una imagen de prueba...")
            img = Image.fromarray((np.random.rand(52, 52, 3) * 255).astype('uint8'))
        
        imagenes_norm[clave] = (1/255.0) * np.array(img).flatten().astype(np.float16)
    
    # 2. Crear la secuencia personalizada
    # Vamos a generar, por ejemplo, 200 muestras totales para que las frecuencias se noten
    total_muestras = 200
    dataset = []

    for i in range(1, total_muestras + 1):
        if i % 5 == 0:
            dataset.append(imagenes_norm["max"])
        elif i % 7 == 0:
            dataset.append(imagenes_norm["duke"])
        else:
            dataset.append(imagenes_norm["doomguy"])

    input_matrix = np.array(dataset)
    print(f"Dataset creado con forma: {input_matrix.shape}")
    # Debería ser algo como (200, 8112)

    # 3. Inicializar y entrenar
    # Nota: vicinity_factor=5.0 ayuda a que las imágenes "compitan" por espacio en el mapa
    som = Kohonen(
        inputs=input_matrix, 
        space_dimension=2, 
        neurons_per_dim=15, # Subimos un poco para ver la separación de los 3 personajes
        learning_constant=0.5, 
        vicinity_factor=3.0
    )
    
    som.calculate_centroids(max_iterations=500)
    
    # 4. Graficar el resultado final
    som.graphicate(size_comun, canales=3)
        