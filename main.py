import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2

def hello_miambiente():
    """Función de ejemplo para demostrar la instalación de paquetes"""
    print("¡Hola desde el ambiente virtual 'miambiente'!")
    
    # Crear un array de ejemplo
    data = np.random.randn(100)
    print(f"Array de ejemplo con media: {np.mean(data):.2f}")
    
    # Crear un DataFrame de ejemplo
    df = pd.DataFrame({
        'x': np.random.randn(100),
        'y': np.random.randn(100)
    })
    print(f"DataFrame creado con {len(df)} filas")
    
    # Crear un gráfico simple
    plt.figure(figsize=(8, 6))
    plt.scatter(df['x'], df['y'], alpha=0.6)
    plt.title('Gráfico de dispersión de ejemplo')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True, alpha=0.3)
    plt.show()

if __name__ == "__main__":
    hello_miambiente()