import numpy as np
import time
import os

# Importaciones locales de tus redes
from MultilayerPerceptron.multilayer import MLPerceptron
from RBFNetwork.rbf_network import RBFNetwork
from KohonenNetwork.kohonen import Kohonen
from HopfieldNetwork.hopfield import Hopfield

class MNISTImplementation:
    mlp: MLPerceptron
    rbf: RBFNetwork
    som: Kohonen
    hopfield_net: Hopfield

    def __init__(self):
        pass

    # ==========================================
    # 1. FUNCIONES DE CARGA Y PREPROCESAMIENTO
    # ==========================================

    def cargar_csv_mnist(self, ruta_csv, max_muestras=None):
        """Carga el CSV de forma eficiente y separa etiquetas de píxeles."""
        if not os.path.exists(ruta_csv):
            raise FileNotFoundError(f"No se encontró el archivo: {ruta_csv}")
            
        print(f"Leyendo {ruta_csv}...")
        # Cargamos solo las filas deseadas si se especifica un límite para agilizar la prueba
        if max_muestras:
            datos = np.loadtxt(ruta_csv, delimiter=',', dtype=np.float32, max_rows=max_muestras)
        else:
            datos = np.loadtxt(ruta_csv, delimiter=',', dtype=np.float32)
            
        etiquetas = datos[:, 0].astype(np.int32)
        imagenes = datos[:, 1:] / 255.0  # Normalización básica [0, 1]
        return imagenes, etiquetas

    def to_one_hot(self, etiquetas, num_clases=10):
        """Convierte etiquetas enteras a vectores One-Hot."""
        return np.eye(num_clases)[etiquetas].astype(np.float16)

    def to_bipolar(self, imagenes_norm):
        """Convierte imágenes [0, 1] a formato bipolar [-1, 1] para Hopfield."""
        return np.where(imagenes_norm > 0.3, 1, -1).astype(np.float16)


    # ==========================================
    # 2. LÓGICA DE EVALUACIÓN POR RED
    # ==========================================

    def evaluar_mlp(self, X_train, Y_train, max_iteraciones, umbral_error):
        print("\n--- Evaluando Perceptrón Multicapa (MLP) ---")
        
        batch_size = X_train.shape[0] 
        feature_size = X_train.shape[1]
        
        # Instanciamos el MLP
        self.mlp = MLPerceptron(
            input_size=batch_size, 
            feature_size=feature_size, 
            learning_constant=0.002, 
            neurons_per_layer=32, 
            hidden_layers=3
        )
        
        # Forzar la última capa a 10 salidas para la clasificación de los dígitos
        from MultilayerPerceptron.sigmoid_layer import SigmoidOutputLayer
        self.mlp.layers[-1] = SigmoidOutputLayer(
            input_size=batch_size, 
            feature_size=32, 
            learning_constant=0.002, 
            neurons=10
        )
        
        # Matriz inicial vacía o con ceros para el parámetro 'result' que pide la firma
        resultado_inicial = np.zeros((batch_size, 10), dtype=np.float16)
        
        inicio = time.time()
        # Enviamos los parámetros tal cual los espera tu arquitectura:
        # inputs, threshold, expected_result, result (adaptado por épocas internamente o iteraciones)
        # Nota: si tu clase sobreescribió la firma revisa si mantiene el orden de Adaline
        resultado = self.mlp.calculate_result(
            inputs=X_train, 
            threshold=umbral_error, 
            expected=Y_train,
            max_iterations=max_iteraciones
        )
        tiempo_ejecucion = time.time() - inicio
        
        mse_evolucion = self.mlp.error_values
        error_final = self.mlp.error_values[-1]

        print(f"Tiempo de ejecución: {tiempo_ejecucion:.4f} s")
        print(f"Error cuadrático medio (MSE) final alcanzado: {error_final:.6f}")
        
        precision_final = 1 - ( (error_final ** 0.5) / 2 )     # 100% - ( Raíz del MSE entre la amplitud de los datos (1 - (-1) = 2) ) 

        return tiempo_ejecucion, (precision_final * 100)


    def evaluar_rbf(self, X_train, Y_train, X_test, Y_test, batch_size):
        print("\n--- Evaluando Red de Base Radial (RBF) ---")
        X_tr, Y_tr = X_train[:batch_size], Y_train[:batch_size]
        X_ts, Y_ts = X_test[:batch_size], Y_test[:batch_size]
        
        # Configuramos la RBF para clasificar: Capa de salida con tamaño 10 (clases)
        # Modificamos dinámicamente el tamaño de la capa de salida para que no sea autodiseñada (784)
        self.rbf = RBFNetwork(input_size=batch_size, feature_size=784, neurons_rbf=20)
        self.rbf.layers[1] = self.rbf.layers[1].__class__(batch_size, 20, 10) # Forzar 10 salidas en RBFOutputLayer
        
        inicio = time.time()
        # Entrenamiento RBF (Centros por K-Means/Aleatorios y pesos por Pseudoinversa)
        self.rbf.calculate_result(X_tr, Y_tr, max_iterations=5)
        tiempo_entrenamiento = time.time() - inicio
        
        # Predicción
        salidas_test, historia, epochs = self.rbf.calculate_result(X_ts, Y_ts, max_iterations=1)
        predicciones = np.argmax(salidas_test, axis=1)
        reales = np.argmax(Y_ts, axis=1)
        precision = np.mean(predicciones == reales) * 100
        
        print(f"Tiempo de entrenamiento: {tiempo_entrenamiento:.4f} s")
        print(f"Precisión en Test: {precision:.2f}%")
        return tiempo_entrenamiento, precision, historia, epochs


    def evaluar_kohonen(self, X_train, etiquetas_train, X_test, etiquetas_test, batch_size=200):
        print("\n--- Evaluando Mapa Autoorganizado de Kohonen (SOM) ---")
        X_tr = X_train[:batch_size]
        X_ts = X_test[:batch_size]
        
        # Grid de 5x5 = 25 neuronas en un espacio de 2 dimensiones
        self.som = Kohonen(inputs=X_tr, space_dimension=2, neurons_per_dim=5, 
                    learning_constant=0.5, vicinity_factor=3.0)
        
        inicio = time.time()
        # Tu método train entrena el mapa de centroides de forma no supervisada
        self.som.calculate_centroids(max_iterations=10)
        tiempo_entrenamiento = time.time() - inicio
        
        # Para medir la precisión en una red No Supervisada:
        # 1. Mapear qué dígito representa cada neurona según el dato de entrenamiento que más la activa
        neurona_a_digito = {}
        # Calculamos activaciones para el set de entrenamiento
        for i in range(batch_size):
            x = X_tr[i]
            # Distancia euclidiana a los pesos de las neuronas
            dists = np.linalg.norm(self.som.weight - x, axis=1)
            bmu = np.argmin(dists) # Neurona ganadora
            if bmu not in neurona_a_digito:
                neurona_a_digito[bmu] = []
            neurona_a_digito[bmu].append(etiquetas_train[i])
            
        # Asignar a cada neurona el dígito mayoritario
        for bmu in neurona_a_digito:
            votos = neurona_a_digito[bmu]
            neurona_a_digito[bmu] = max(set(votos), key=votos.count)
            
        # 2. Evaluar el set de prueba usando el mapa construido
        aciertos = 0
        for i in range(len(X_ts)):
            x_t = X_ts[i]
            dists = np.linalg.norm(self.som.weight - x_t, axis=1)
            bmu = np.argmin(dists)
            
            prediccion = neurona_a_digito.get(bmu, -1) # Si la neurona nunca se activó, asigna -1
            if prediccion == etiquetas_test[i]:
                aciertos += 1
                
        precision = (aciertos / len(X_ts)) * 100
        print(f"Tiempo de entrenamiento: {tiempo_entrenamiento:.4f} s")
        print(f"Precisión mediante Clustering: {precision:.2f}%")
        return tiempo_entrenamiento, precision


    def evaluar_hopfield(self, X_train, etiquetas_train, X_test, etiquetas_test):
        print("\n--- Evaluando Red de Hopfield ---")
        
        # Convertir a bipolar
        X_train_bip = self.to_bipolar(X_train)
        X_test_bip = self.to_bipolar(X_test[:100]) # Evaluamos sobre 100 imágenes de test
        etiquetas_ts = etiquetas_test[:100]
        
        # Hopfield colapsa si almacena muchos patrones. Vamos a extraer 10 patrones ideales (el "promedio" de cada dígito)
        patrones_ideales = []
        for digito in range(10):
            indices = np.where(etiquetas_train == digito)[0]
            if len(indices) > 0:
                promedio = np.mean(X_train_bip[indices], axis=0)
                patron_bipolar = np.where(promedio > 0, 1, -1).astype(np.float16)
                patrones_ideales.append(patron_bipolar)
            else:
                patrones_ideales.append(np.ones(784, dtype=np.float16))
                
        patrones_ideales = np.array(patrones_ideales) # Forma (10, 784)
        
        inicio = time.time()
        # Inicialización de la red con los 10 dígitos conocidos
        self.hopfield_net = Hopfield(inputs=patrones_ideales)
        tiempo_entrenamiento = time.time() - inicio # En Hopfield es instantáneo (cálculo directo de pesos)
        
        # ========================================================
        # CAPTURA DE VECTORES PARA LA GRÁFICA DE HOPIFIELD (MNIST)
        # ========================================================
        # Tomamos la primera muestra ruidosa del test (noisy)
        muestra_test_ruidosa = X_test_bip[0]
        clase_real = etiquetas_ts[0]
        # El patrón ideal de entrenamiento correspondiente a ese dígito (original)
        patron_original_ideal = patrones_ideales[clase_real]
        
        # Obtenemos la respuesta de la red iterativa (recovered)
        # Nota: iterate() devuelve una tupla/arreglo, extraemos la primera fila indexando [0] si aplica
        resultado_iteracion = self.hopfield_net.iterate(muestra_test_ruidosa, max_iterations=5)
        muestra_recuperada = resultado_iteracion[0] if resultado_iteracion.ndim > 1 else resultado_iteracion


        # Evaluar la capacidad de reconocimiento (recuperación de patrones)
        aciertos = 0
        for i in range(len(X_test_bip)):
            test_img = X_test_bip[i]
            # Recuperar patrón iterando la red dinámica
            imagen_recuperada = self.hopfield_net.iterate(test_img, max_iterations=5)
            
            # Comparar el vector recuperado contra los 10 patrones ideales para ver a cuál se parece más
            distancias = [np.linalg.norm(imagen_recuperada - patron) for patron in patrones_ideales]
            digito_predicho = np.argmin(distancias)
            
            if digito_predicho == etiquetas_ts[i]:
                aciertos += 1
                
        precision = (aciertos / len(X_test_bip)) * 100
        print(f"Tiempo de 'Entrenamiento' (Almacenamiento): {tiempo_entrenamiento:.6f} s")
        print(f"Precisión en Asociación de Dígitos: {precision:.2f}%")
        return tiempo_entrenamiento, precision, patron_original_ideal, muestra_test_ruidosa, muestra_recuperada


# ==========================================
# 3. BLOQUE PRINCIPAL DE EJECUCIÓN
# ==========================================

if __name__ == "__main__":
    mnist = MNISTImplementation()
    
    # Definir rutas de los archivos (ajusta si se encuentran en subcarpetas)
    ruta_train = "./MNISTImplementation/Data/mnist_train.csv" 
    ruta_test = "./MNISTImplementation/Data/mnist_test.csv"
    
    # Cargamos una porción inicial de datos para asegurar fluidez en las operaciones de matrices
    # Puedes aumentar estos números si tu máquina procesa holgadamente matrices grandes en NumPy float16
    X_train, etiquetas_train = mnist.cargar_csv_mnist(ruta_train, max_muestras=2000)
    X_test, etiquetas_test = mnist.cargar_csv_mnist(ruta_test, max_muestras=500)
    
    Y_train_oh = mnist.to_one_hot(etiquetas_train)
    Y_test_oh = mnist.to_one_hot(etiquetas_test)
    
    # Diccionario para consolidar métricas finales
    resultados = {}
    
    # 1. Perceptrón Multicapa
    t_mlp, p_mlp = mnist.evaluar_mlp(X_train, Y_train_oh, max_iteraciones=1000, umbral_error=0.02)
    resultados['MLP'] = {'Tiempo': t_mlp, 'Precision': p_mlp}
    
    # 2. Red de Base Radial
    t_rbf, p_rbf, story_rbf, epochs_rbf  = mnist.evaluar_rbf(X_train, Y_train_oh, X_test, Y_test_oh, batch_size=100)
    resultados['RBF'] = {'Tiempo': t_rbf, 'Precision': p_rbf}
    
    # 3. Mapa de Kohonen
    t_som, p_som = mnist.evaluar_kohonen(X_train, etiquetas_train, X_test, etiquetas_test, batch_size=200)
    resultados['Kohonen (SOM)'] = {'Tiempo': t_som, 'Precision': p_som}
    
    # 4. Red de Hopfield
    t_hop, p_hop, original_hop, noisy_hop, rec_hop = mnist.evaluar_hopfield(X_train, etiquetas_train, X_test, etiquetas_test)
    resultados['Hopfield'] = {'Tiempo': t_hop, 'Precision': p_hop}
    
    # ==========================================
    # TABLA COMPARATIVA FINAL
    # ==========================================
    print("\n" + "="*50)
    print(f"{'RED NEURONAL':<20} | {'TIEMPO (s)':<12} | {'PRECISIÓN (%)':<12}")
    print("="*50)
    for red, metricas in resultados.items():
        print(f"{red:<20} | {metricas['Tiempo']:<12.4f} | {metricas['Precision']:<12.2f}")
    print("="*50)

    # =========================================
    # GRAFICAR
    # =========================================
   
    mnist.mlp.graphicate()
    mnist.rbf.graficar_evolucion(story_rbf, img_size=(28, 28), pasos=min(epochs_rbf, 5), canales=1)
    mnist.som.graphicate(img_size=(28, 28), canales=1) # Tamaño imágenes MNIST
    mnist.hopfield_net.graphicate(original_hop, noisy_hop, rec_hop, shape=(28, 28))
