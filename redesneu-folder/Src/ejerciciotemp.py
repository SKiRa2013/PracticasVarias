from Src.adeline import AdelineLayer
import numpy as np

if __name__ == "__main__":
    # Kelvin y Fahrenheit, necesito que me regrese Celsius
    entradas = np.array([
        [233.15, -40.0],
        [263.15, 14.0],
        [273.15, 32.0],
        [283.15, 50.0],
        [293.15, 68.0],
        [298.15, 77.0],
        [303.15, 86.0],
        [310.15, 98.6],
        [318.15, 113.0],
        [333.15, 140.0],
        [353.15, 176.0],
        [373.15, 212.0],
        [423.15, 302.0],
        [473.15, 392.0],
        [573.15, 572.0]
    ])
    
    # Kelvin a Celsius y Fahrenheit a Celsius, deben coincidir
    respuesta_esperada = np.array([
        [-40, -40],
        [-10, -10],
        [0, 0],
        [10, 10],
        [20, 20],
        [25, 25],
        [30, 30],
        [37, 37],
        [45, 45],
        [60, 60],
        [80, 80],
        [100, 100],
        [150, 150],
        [200, 200],
        [300, 300]
    ])

    # ---------------------------------------------------------
    #  Por la magnitud de los datos, es obligatorio normalizar
    # ---------------------------------------------------------
    
    max_entradas = np.max(entradas)
    max_expected = np.max(respuesta_esperada)
    
    entradas_norm = (1 / max_entradas) * entradas
    expected_norm = (1 / max_expected) * respuesta_esperada
    
    # --------------------------------------------------------
    
    adenalina = AdelineLayer(input_size=np.shape(entradas_norm)[0], feature_size=np.shape(entradas_norm)[1], learning_constant=0.1, neurons=2)
    adenalina.set_weight([[0.89, 1.04], [0.51, 0.61]])
    adenalina.set_bias((1 / max_expected) * np.full((15, 2), [273, -10]))

    resultado = adenalina.activation(entradas_norm)

    print(f"Batch de entradas:\n{entradas_norm}\n")
    print(f"Pesos iniciales:\n{adenalina.weight}\n")
    print(f"Sesgo:\n{adenalina.bias}\n")
    print(f"Resultados (normalizado):\n{resultado}\n\n")

    resultado_final = adenalina.calculate_result(inputs=entradas_norm, threshold=0.000033, expected_result=expected_norm, result=resultado)
    
    print(f"\nResultado final:\n{max_expected * resultado_final}\n")
    print(f"\nResultado buscado:\n{respuesta_esperada}")