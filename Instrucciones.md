# Instrucciones para crear y usar ambientes virtuales con Conda

## Objetivo
Aprender a crear, gestionar y usar ambientes virtuales en Conda para proyectos de Python, incluyendo la instalación de paquetes y la creación de código.

## Prerrequisitos
- Tener Anaconda instalado en tu sistema
- Conocimientos básicos de Python
- Familiaridad con la línea de comandos

## Paso 1: Abrir Anaconda Prompt
**IMPORTANTE**: Usa **Anaconda Prompt**. También puedes usar WindowsPowerShell pero debes configurarlo apropiadamente.

1. Busca "Anaconda Prompt" en el menú de inicio de Windows
2. Se abrirá una ventana de terminal con el entorno de Anaconda configurado

## Paso 2: Crear el ambiente virtual
En Anaconda Prompt, ejecuta el siguiente comando para crear un ambiente virtual llamado "miambiente":

```bash
conda create --name miambiente python=3.9
```

- `--name miambiente`: Define el nombre del ambiente
- `python=3.9`: Especifica la versión de Python (puedes usar 3.8, 3.10, 3.11 según prefieras)

Cuando te pregunte si proceder, escribe `y` y presiona Enter.

## Paso 3: Activar el ambiente virtual
Una vez creado, activa el ambiente:

```bash
conda activate miambiente
```

Deberías ver `(miambiente)` al inicio de la línea de comandos, indicando que el ambiente está activo.

## Paso 4: Instalar paquetes usando requirements.txt
Crea un archivo `requirements.txt` en tu directorio de trabajo con el siguiente contenido:

```txt
numpy==1.24.3
pandas==2.0.3
matplotlib==3.7.2
jupyter==1.0.0
opencv-python==4.8.0.76
pillow==10.0.0
```

Luego instala todos los paquetes de una vez:

```bash
pip install -r requirements.txt
```

## Paso 5: Verificar la instalación
Verifica que los paquetes se instalaron correctamente:

```bash
conda list
```

O para ver solo los paquetes instalados con pip:

```bash
pip list
```

## Paso 6: Crear archivos de código

### Archivo Python (.py)
Crea un archivo llamado `main.py` con el siguiente código de ejemplo:

```python
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
```

### Cuaderno Jupyter (.ipynb)
Crea un cuaderno llamado `ejercicio.ipynb` con la siguiente estructura básica:

**Celda 1 (Markdown):** Título del ejercicio con tu nombre y fecha
**Celda 2 (Markdown):** Descripción de lo que vas a hacer
**Celda 3 (Markdown):** Explicación del primer paso
**Celda 4 (Código):** Código para importar librerías
**Celda 5 (Markdown):** Explicación del segundo paso
**Celda 6 (Código):** Código para crear datos o realizar análisis
**Celda 7 (Markdown):** Explicación del tercer paso
**Celda 8 (Código):** Código para visualización o procesamiento
**Celda 9 (Markdown):** Conclusiones y aprendizajes

**Importante**: 
- Usa celdas de texto (markdown) para explicar cada paso
- Crea código original y diferente al archivo `main.py`
- Demuestra tu comprensión de los paquetes instalados
- Incluye al menos 3-4 celdas de código con diferentes funcionalidades

### Archivo .gitignore
Crea un archivo llamado `.gitignore` en tu directorio de trabajo. Puedes usar como referencia el archivo `.gitignore` que ya está creado en este repositorio.

## Paso 7: Ejecutar el código

### Ejecutar el archivo Python
```bash
python main.py
```

### Ejecutar Jupyter Notebook
```bash
jupyter notebook
```

Esto abrirá Jupyter en tu navegador web. Navega hasta el archivo `ejercicio.ipynb` y ejecuta las celdas una por una para verificar que tu código funciona correctamente.

## Paso 8: Desactivar el ambiente
Cuando termines de trabajar, desactiva el ambiente:

```bash
conda deactivate
```

## Paso 9: Gestionar el ambiente

### Listar todos los ambientes
```bash
conda env list
```

### Eliminar el ambiente (si es necesario)
```bash
conda env remove --name miambiente
```

### Exportar el ambiente
```bash
conda env export > environment.yml
```

### Recrear el ambiente desde el archivo
```bash
conda env create -f environment.yml
```

## Comandos útiles adicionales

### Ver información del ambiente actual
```bash
conda info
```

### Actualizar conda
```bash
conda update conda
```

### Buscar paquetes disponibles
```bash
conda search nombre_paquete
```

### Instalar paquetes específicos
```bash
conda install nombre_paquete
# o
pip install nombre_paquete
```

## Solución de problemas comunes

### Error: "conda no se reconoce como comando"
- Asegúrate de usar Anaconda Prompt, no la terminal normal de Windows
- Verifica que Anaconda esté instalado correctamente

### Error al instalar paquetes
- Verifica que el ambiente esté activado (debe aparecer `(miambiente)` al inicio)
- Intenta usar `pip install` en lugar de `conda install` para algunos paquetes
- Verifica que tengas conexión a internet

### Problemas con Jupyter
- Asegúrate de que `jupyter` esté instalado en el ambiente activo
- Si hay problemas, reinstala: `pip install --force-reinstall jupyter`

## Tarea

Desarrolla las siguientes actividades. Genera los archivos correspondientes en el repositorio. Documenta los pasos realizados en el README.

1. Crear el ambiente virtual "miambiente"
2. Instalar paquetes desde requirements.txt
3. Crear y ejecutar un archivo main.py. La funcionalidad de este archivo es libre y el propósito es mostrar la ejecución de un archivo .py en un ambiente virtual.
4. Crear y ejecutar ejercicio.ipynb. La funcionalidad de este archivo es libre y el propósito es mostrar la ejecución de un archivo .ipynb en un ambiente virtual.
5. Crear archivo .gitignore apropiado
6. Explicar qué es .gitignore y cómo funciona en el README.md
7. Incluir información sobre el uso de IA para el desarrollo de la actividad (ALTO, MEDIO, BAJO, NINGUNO, y explicar la asignación de esta valoración)

## Recursos adicionales
- [Documentación oficial de Conda](https://docs.conda.io/)
- [Guía de ambientes virtuales](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
- [Tutorial de Jupyter](https://jupyter.org/try)