from RBFNetwork.rbf_layer import RBFLayer, RBFOutputLayer
from MultilayerPerceptron.multilayer import MLPerceptron

import matplotlib.pyplot as plt
from PIL import Image

import numpy as np
import numpy.typing as npt

class RBFNetwork(MLPerceptron):
    def __init__(self, input_size: int, feature_size: int, neurons_rbf: int):
        super().__init__(input_size, feature_size, 0, neurons_rbf, 0)

    def initialize_perceptron(self):
        """
        Sobreescribimos la inicialización para asegurar la estructura RBF:
        1. Una capa RBF (oculta)
        2. Una capa de salida
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

    def calculate_result(self, inputs: npt.NDArray, expected: npt.NDArray, max_iterations: int) -> tuple[npt.NDArray[np.float16], list, int]:
        hidden_layer: RBFLayer = self.layers[0]
        output_layer: RBFOutputLayer = self.layers[1]

        # Inicializamos los pesos de la capa oculta con datos reales
        indices_aleatorios = np.random.choice(inputs.shape[0], hidden_layer.neurons, replace=False)
        hidden_layer.weight = inputs[indices_aleatorios].T.copy()

        # Guardaremos una "foto" de la reconstrucción aquí
        historia_reconstruccion = []
        historia_reconstruccion.append(np.copy(hidden_layer.weight.T))

        for epoch in range(1, max_iterations + 1):
            # Centroides finales (k-means), también detecta si se mantuvieron igual
            updated_centers = hidden_layer.update_centers(inputs)

            # Se recalcula sigma en base a los nuevos centroides
            hidden_layer.calculate_sigma()
            
            # Generamos la matriz de pseudomuestras
            g_matrix = hidden_layer.activation(inputs)
            output_layer.solve_pseudo_inverse(g_matrix, expected)

            # --- CAPTURA DE ÉPOCA ---
            # Guardamos la predicción actual para los índices elegidos
            historia_reconstruccion.append(np.copy(hidden_layer.weight.T))
            
            # Evaluar si los centroides se mantuvieron igual
            result = output_layer.activation(g_matrix)
            # result = self.forward(g_matrix)
            
            if not updated_centers:
                print(f"Convergió por centros y pesos en epoch {epoch}.")
                return result, historia_reconstruccion, epoch

        print(f"¡ALERTA! Se alcanzó el número máximo de epochs: {max_iterations}")
        return result, historia_reconstruccion, max_iterations

    def graficar_evolucion(self, historia, img_size, canales, pasos=5):
        """
        Orientación:
        - Filas: Momentos en el tiempo (Épocas)
        - Columnas: Neuronas (Prototipos)
        """
        total_pasos = len(historia)
        n_neuronas = historia[0].shape[0]
        
        # Seleccionamos los índices de las épocas
        pasos_idx = np.linspace(0, total_pasos - 1, pasos, dtype=int)
        
        # Invertimos: Filas = Épocas, Columnas = Neuronas
        fig, axes = plt.subplots(pasos, n_neuronas, 
                                figsize=(n_neuronas * 2.5, pasos * 3))
        
        # Asegurar que axes sea siempre 2D (caso de una sola neurona o época)
        if pasos == 1: axes = np.expand_dims(axes, axis=0)
        if n_neuronas == 1: axes = np.expand_dims(axes, axis=1)

        for row_idx, p_idx in enumerate(pasos_idx):
            pesos_epoca = historia[p_idx]
            
            for col_idx in range(n_neuronas):
                ax = axes[row_idx, col_idx]
                
                # Reconstruir imagen del peso (centroide)
                img = pesos_epoca[col_idx].reshape(img_size[1], img_size[0], canales)
                
                # Mostrar imagen
                ax.imshow(np.clip(img.astype(np.float32), 0, 1))
                
                # Etiqueta de Época solo en la primera columna
                if col_idx == 0:
                    ax.set_ylabel(f"Época {row_idx}", fontsize=12, fontweight='bold')
                
                # Etiqueta de Neurona solo en la primera fila
                if row_idx == 0:
                    ax.set_title(f"Neurona {col_idx}", fontsize=10)
                
                ax.axis('off')

        plt.tight_layout()
        plt.suptitle("Evolución Temporal de los Prototipos RBF (Vertical)", fontsize=16, y=0.96)
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
    
    # 2. Crear el dataset
    dataset_limpio = []
    dataset_ruidoso = []
    total_muestras = 100

    for i in range(total_muestras):
        # Elegir un personaje al azar
        claves = list(imagenes_norm.keys())
        seleccion = np.random.choice(claves)
        p = imagenes_norm[seleccion]
        dataset_limpio.append(p)
        
        # Crear "Pseudomuestra": Imagen + Ruido Gaussiano
        ruido = np.random.normal(0, 0.3, p.shape).astype(np.float16)
        dataset_ruidoso.append(np.clip(p + ruido, 0, 1))

    X = np.array(dataset_ruidoso)
    Y = np.array(dataset_limpio) # La red debe aprender a limpiar el ruido

    # 3. Inicializar RBF
    red_rbf = RBFNetwork(
        input_size=total_muestras,
        feature_size=feature_size,
        neurons_rbf=5,
    )

    # 4. Entrenar
    result, story, epoch = red_rbf.calculate_result(X, Y, max_iterations=100)

    # 5. Graficar
    red_rbf.graficar_evolucion(story, img_size=size_comun, pasos=min(epoch, 5), canales=3)
    