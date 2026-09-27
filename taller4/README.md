# Transformaciones de Intensidad en Imágenes

**Curso:** Visión por Computador
Ochoa Lechuga

Tarea sobre **transformaciones puntuales de intensidad**: operaciones que calculan cada píxel de salida usando solo el valor del mismo píxel de entrada, $s = T(r)$. Se estudian transformaciones lineales, por tramos y gamma, primero en escala de grises y luego aplicadas de forma independiente a los canales R, G y B de imágenes a color. En cada ejercicio se muestran la imagen original y la transformada, sus histogramas (por canal en RGB), una tabla de estadísticas y una interpretación con las respuestas a las preguntas.

---

## Estructura del repositorio

```
tarea-transformaciones-intensidad/
├── README.md                          # Este archivo
├── requirements.txt                   # Dependencias de Python
├── transformaciones_intensidad.ipynb  # Notebook principal con los 15 ejercicios (ya ejecutado)
├── generar_imagenes.py                # (Opcional) regenera las imágenes de imagenes/
├── src/
│   ├── __init__.py
│   ├── transformaciones.py            # Transformaciones y métricas
│   └── visualizacion.py               # Figuras: imágenes + histogramas, curvas, tablas
└── imagenes/
    ├── gris.png                       # Fotógrafo, escala de grises, rango completo
    ├── bajo_contraste.png             # Superficie lunar, bajo contraste (ejercicio 2)
    ├── oscura.png                     # Taza de café subexpuesta (ejercicios 4 y 7)
    ├── color.png                      # Taza de café, RGB
    └── color2.png                     # Astronauta, RGB
```

### Módulos de apoyo (`src/`)

Para que el notebook muestre solo lo esencial de cada ejercicio, la lógica está en dos módulos:

**`src/transformaciones.py`**

| Función | Descripción |
|---|---|
| `cargar_gris`, `cargar_rgb` | Leen imágenes con OpenCV; `cargar_rgb` convierte de BGR a RGB |
| `a_uint8(img, modo)` | Lleva un resultado flotante a `[0, 255]` por **clipping** o **normalización min-max** |
| `lineal(img, a, b)` | $I' = aI + b$ |
| `por_tramos(img, puntos)` | Función lineal por partes definida por puntos de control (LUT) |
| `inversion(img)` | $I' = 255 - I$ |
| `gamma(img, g, c)` | $I' = 255\,c\,(I/255)^{\gamma}$ |
| `curva_gamma`, `ajuste_lineal_a_gamma` | Curva gamma y su mejor aproximación lineal por mínimos cuadrados |
| `lineal_canales`, `gamma_canales` | Transformación lineal o gamma con parámetros distintos por canal |
| `eliminar_canal`, `intercambiar_canales`, `a_gris` | Operaciones sobre canales y conversión a luminancia |
| `estadisticas`, `detalle_en_sombras` | Métricas usadas en las interpretaciones |

Todas las operaciones se calculan en `float64` para evitar el desbordamiento de `uint8` (en `uint8`, `200 + 100` da `44`), y la conversión final al rango válido se hace siempre de forma explícita.

**`src/visualizacion.py`**

| Función | Descripción |
|---|---|
| `comparar(lista)` | Fila de imágenes con su histograma debajo (una curva por canal en RGB). Si hay picos de saturación en 0 o 255, se indica su porcentaje en el gráfico para que no aplasten el resto del histograma |
| `curvas(dict)` | Gráfica de funciones de transferencia $s = T(r)$ con la identidad como referencia |
| `tabla(lista)` | Tabla con media, desviación estándar, mínimo, máximo, % de píxeles en 0 y en 255 y número de niveles distintos |

---

## Ejecución

### Requisitos

- Python 3.9 o superior
- Paquetes: `numpy`, `opencv-python`, `matplotlib`, `jupyter` (y `scikit-image` solo si se quieren regenerar las imágenes)

### Opción A: Anaconda 

```bash
conda create -n vc-intensidad python=3.11 -y
conda activate vc-intensidad
pip install -r requirements.txt
jupyter notebook transformaciones_intensidad.ipynb
```

### Opción B: entorno virtual con `venv`

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
jupyter notebook transformaciones_intensidad.ipynb
```

El notebook **debe abrirse desde la carpeta raíz del repositorio**, porque importa los módulos con `from src.transformaciones import ...` y lee las imágenes de `imagenes/`. Para reproducir los resultados, ejecutar **Kernel → Restart & Run All**. La ejecución completa tarda menos de un minuto.

El notebook se entrega **ya ejecutado**, así que todas las figuras, tablas e interpretaciones se pueden ver directamente en GitHub sin ejecutar nada.

### Regenerar las imágenes (opcional)

Las imágenes ya están en `imagenes/`. Si se borran o se quieren regenerar:

```bash
pip install scikit-image
python generar_imagenes.py
```

Para usar imágenes propias, basta con reemplazar los archivos de `imagenes/` conservando los nombres (las interpretaciones del notebook se refieren a las imágenes originales, así que habría que actualizarlas).

---

## Imágenes utilizadas

Todas provienen del conjunto de imágenes de ejemplo de `scikit-image` (`skimage.data`), de libre uso.

| Archivo | Origen | Uso |
|---|---|---|
| `gris.png` | `data.camera()` | Partes 1 y 2: imagen en gris con rango completo y zonas oscuras, medias y claras bien diferenciadas |
| `bajo_contraste.png` | `data.moon()` | Ejercicio 2: el 97 % de los píxeles está entre 78 y 141, con unos pocos valores atípicos en 0 y 255 |
| `oscura.png` | `data.coffee()` oscurecida con $255\,(I/255)^{3}$ | Ejercicios 4 y 7: simula una foto subexpuesta (brillo medio 43/255) que conserva los reflejos claros |
| `color.png` | `data.coffee()` | Parte 3: colores cálidos, predominio del canal rojo |
| `color2.png` | `data.astronaut()` | Parte 3: colores saturados variados (naranja, azul, rojo, blanco) |

---

## Contenido de la actividad

### Parte 1: Transformaciones lineales (escala de grises)

| Ejercicio | Contenido | Resultado principal |
|---|---|---|
| 1. Lineal básica | $I' = aI + b$ con seis combinaciones de $(a, b)$ | $a$ escala las diferencias (contraste), $b$ desplaza el histograma (brillo); ambos saturan fácilmente |
| 2. Saturación | Clipping vs normalización en $2I - 60$ y en un estiramiento de contraste de la luna | El clipping pierde información en los extremos; la normalización puede anular la transformación y es sensible a atípicos |
| 3. Por tramos | Curva en S que oscurece bajos, fija el centro y aclara altos | Expande tonos medios y comprime los extremos: más contraste con muy poca saturación |
| 4. Inversión | $I' = 255 - I$ | El histograma se refleja; la desviación no cambia; útil para detalles claros sobre fondos oscuros (radiografías, astronomía) |

### Parte 2: Transformaciones no lineales (gamma)

| Ejercicio | Contenido | Resultado principal |
|---|---|---|
| 5. Corrección gamma | $\gamma = 0.3, 0.5, 1.5, 2.5$ y análisis de la pendiente | $\gamma<1$ expande sombras y aclara; $\gamma>1$ expande luces y oscurece |
| 6. Gamma vs lineal | Recta de mínimos cuadrados que aproxima la gamma | Se parecen en promedio, pero una recta tiene pendiente constante y no puede redistribuir el contraste |
| 7. Imagen oscura | Lineal sin saturar, lineal y gamma con el mismo brillo medio | La gamma recupera las sombras sin saturar las luces; la lineal satura el 74 % de los píxeles |

### Parte 3: Transformaciones en imágenes RGB

| Ejercicio | Contenido |
|---|---|
| 8. Lineal por canal | Tres configuraciones de $(a_R, a_G, a_B)$ y $(b_R, b_G, b_B)$ sobre dos imágenes |
| 9. Un solo canal | Cambios de $a$ y $b$ solo en R, con análisis de tono y saturación en HSV |
| 10. Eliminar un canal | $R=0$, $G=0$, $B=0$ en imágenes reales y en una paleta de colores básicos |
| 11. Gamma por canal | Tres combinaciones de $(\gamma_R, \gamma_G, \gamma_B)$ y su efecto sobre los grises |
| 12. Intercambio de canales | $R \leftrightarrow B$ y $R \leftrightarrow G$; relación con el orden BGR de OpenCV |
| 13. Gris vs RGB | Colores distintos con el mismo gris; conteo de colores que se fusionan en cada nivel |
| 14. Histogramas por canal | Traslación en R, compresión en G y gamma en B, con sus histogramas antes y después |
| 15. Estilos visuales | Transformaciones para imagen cálida, fría y de alto contraste, con sus curvas y justificación |

El notebook termina con una sección de **conclusiones** y la **declaración de uso de IA**.

---

## Declaración de uso de herramientas de Inteligencia Artificial

# Nivel de uso de la IA: Medio
1. Imagenes: la ia se uso para conseguir imagenes de uso libre para el desarrollo de la actividad 
2. Investigación: para busqueda de información y uso de las funciones de las librerias
3. Escritura: para mejorar la redaccion y agregar comentarios que la IA considere necesarios 
4. Verificación del codigo 
5. Corregir errores durante el desarrollo del taller