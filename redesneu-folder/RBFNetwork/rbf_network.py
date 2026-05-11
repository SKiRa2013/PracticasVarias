from RBFNetwork.rbf_layer import RBFLayer, RBFOutputLayer
from MultilayerPerceptron.multilayer import MLPerceptron

import matplotlib.pyplot as plt
from PIL import Image

import numpy as np
import numpy.typing as npt

class RBFNetwork(MLPerceptron):
    def __init__(self, input_size: int, feature_size: int, neurons_rbf: int):
        super().__init__(input_size, feature_size, 0, neurons_rbf, hidden_layers=0)

    def initialize_perceptron(self):
        """
        Sobreescribimos la inicialización para asegurar la estructura RBF:
        1. Una capa RBF (oculta)
        2. Una capa de salida (Adaline o Sigmoide)
        """
        # Capa 1: RBF
        self.layers.append(RBFLayer(
            self.input_size, 
            self.feature_size, 
            self.neurons_per_layer
        ))

        # Capa 2: Salida (Usamos tu SigmoidOutputLayer existente)
        # Esta capa sí aprenderá usando el delta_output y los pesos.
        self.layers.append(RBFOutputLayer(
            self.input_size, 
            self.neurons_per_layer,  
            self.input_size
        ))

    def calculate_result(self, inputs: npt.NDArray, expected: npt.NDArray, max_iterations: int) -> npt.NDArray[np.float16]:
        hidden_layer: RBFLayer = self.layers[0]
        output_layer: RBFOutputLayer = self.layers[1]

        for epoch in range(1, max_iterations + 1):
            # Centroides finales (k-means), también detecta si se mantuvieron igual
            updated_centers = hidden_layer.update_centers(inputs)

            # Se recalcula sigma en base a los nuevos centroides
            hidden_layer.calculate_sigma()
            
            # Generamos la matriz de pseudomuestras
            g_matrix = hidden_layer.activation(inputs)
            output_layer.solve_pseudo_inverse(g_matrix, expected)
            
            # Evaluar si los centroides se mantuvieron igual
            result = output_layer.activation(g_matrix)
            
            if not updated_centers:
                print(f"Convergió por centros y pesos en epoch {epoch}.")
                return result

        print(result)
        raise RuntimeError(f"Se alcanzó el número máximo de epochs: {max_iterations}")
    
    def graphicate(self, img_size: tuple[int, int]):
        # Accedemos a la capa RBF (la primera)
        rbf_layer = self.layers[0]
        neurons = rbf_layer.neurons
        
        # Determinar la geometría de la rejilla (cuadrada o lo más cercana posible)
        side = int(np.ceil(np.sqrt(neurons)))
        rows, cols = side, side 

        fig, axes = plt.subplots(rows, cols, figsize=(12, 12))
        axes_flat = axes.flatten()

        # Los centros están en rbf_layer.weight (feature_size, neurons)
        # Transponemos para iterar por cada centroide (imagen)
        centros_imagenes = rbf_layer.weight.T 

        for i in range(neurons):
            ax = axes_flat[i]
            try:
                # Reconstrucción RGB: (alto, ancho, 3)
                # weight[i] tiene tamaño 8112
                imagen_neurona = centros_imagenes[i].reshape((img_size[1], img_size[0], 3))
                
                # Clipping para asegurar que los colores sean válidos [0, 1]
                imagen_visual = np.clip(imagen_neurona.astype(np.float32), 0, 1)
                
                ax.imshow(imagen_visual)
                ax.set_title(f"Centro {i+1}", fontsize=8)
            except Exception as e:
                pass
            ax.axis('off')

        # Limpiar subplots vacíos
        for j in range(i + 1, len(axes_flat)):
            axes_flat[j].axis('off')

        plt.subplots_adjust(wspace=0.1, hspace=0.3)
        plt.suptitle("RBF Network: Visualización de Centros (Prototipos de Imágenes)")
        plt.show()


if __name__ == "__main__":
    personajes = {
        "doomguy": "doomguy.png",
        "max": "maxdamage.png",
        "duke": "dukenukem.png",
        "blazkowicz": "blazkowicz.png",
    }
    
    imagenes_norm = {}
    size_comun = (52, 52)
    feature_size = size_comun[0] * size_comun[1] * 3

    # 1. Carga y preprocesamiento
    for clave, nombre in personajes.items():
        try:
            # Buscamos en la carpeta .media
            ruta = f".media/{nombre}"
            img = Image.open(ruta).convert('RGB').resize(size_comun)
        except FileNotFoundError:
            print(f"No se encontró {nombre}, generando ruido para pruebas...")
            img = Image.fromarray((np.random.rand(size_comun[0], size_comun[1], len(personajes)) * 255).astype('uint8'))
        
        # Aplanamos y normalizamos a [0, 1]
        imagenes_norm[clave] = (1/255.0) * np.array(img).flatten().astype(np.float16)
    
    # 2. Crear el dataset (Misma lógica que usaste en SOM)
    total_muestras = 100
    dataset = []
    for i in range(1, total_muestras + 1):
        if i % 3 == 0:
            dataset.append(imagenes_norm["max"])
        elif i % 4 == 0:
            dataset.append(imagenes_norm["duke"])
        elif i % 5 == 0:
            dataset.append(imagenes_norm["doomguy"])
        else:
            dataset.append(imagenes_norm["blazkowicz"])

    input_matrix = np.array(dataset)
    # Para una RBF autoasociativa, la salida esperada es la misma entrada
    expected_output = input_matrix 

    print(f"Dataset de imágenes listo: {input_matrix.shape}") # (100, 8112)

    # 3. Inicializar RBF
    # Usaremos, por ejemplo, 16 neuronas para ver 16 "versiones" o prototipos
    red_rbf = RBFNetwork(
        input_size=total_muestras, 
        feature_size=feature_size, 
        neurons_rbf=16
    )

    # 4. Entrenar
    # Aquí los centros se moverán hacia Doomguy, Duke y Max
    # y la pseudoinversa aprenderá a reconstruirlos.
    red_rbf.calculate_result(
        input_matrix, 
        expected_output, 
        max_iterations=100
    )

    # 5. Graficar los centros (Lo que la red "cree" que son las imágenes base)
    red_rbf.graphicate(size_comun)
