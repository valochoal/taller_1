"""
Transformaciones puntuales de intensidad para imágenes en escala de grises y RGB.

Todas las funciones reciben imágenes como arreglos de NumPy (uint8 o float) y
trabajan internamente en punto flotante (float64) para no perder precisión ni
sufrir desbordamientos (overflow) de uint8. La conversión final al rango
[0, 255] se hace de forma explícita con `a_uint8`, eligiendo entre recorte
(clipping) o normalización.

Convención de canales: las imágenes a color se manejan en orden RGB
(OpenCV lee en BGR; `cargar_rgb` hace la conversión).
"""

from pathlib import Path

import cv2
import numpy as np

RUTA_IMAGENES = Path(__file__).resolve().parent.parent / "imagenes"


# ---------------------------------------------------------------------------
# Carga de imágenes
# ---------------------------------------------------------------------------
def _ruta(nombre):
    ruta = Path(nombre)
    if not ruta.exists():
        ruta = RUTA_IMAGENES / nombre
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró la imagen: {nombre}")
    return str(ruta)


def cargar_gris(nombre):
    """Lee una imagen y la devuelve en escala de grises (uint8, 2D)."""
    return cv2.imread(_ruta(nombre), cv2.IMREAD_GRAYSCALE)


def cargar_rgb(nombre):
    """Lee una imagen y la devuelve en orden RGB (uint8, HxWx3)."""
    bgr = cv2.imread(_ruta(nombre), cv2.IMREAD_COLOR)
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)


# ---------------------------------------------------------------------------
# Conversión al rango [0, 255]
# ---------------------------------------------------------------------------
def a_uint8(img, modo="clip"):
    """
    Lleva una imagen en punto flotante al rango [0, 255] como uint8.

    modo="clip":  recorta; todo lo < 0 pasa a 0 y todo lo > 255 pasa a 255.
    modo="norm":  normalización min-max lineal: (I - min) / (max - min) * 255.
                  Si la imagen es a color, se usa el mínimo y máximo globales
                  (de los tres canales) para no alterar el balance de color.
    """
    img = np.asarray(img, dtype=np.float64)
    if modo == "clip":
        salida = np.clip(img, 0, 255)
    elif modo == "norm":
        mn, mx = img.min(), img.max()
        if mx - mn < 1e-12:
            salida = np.zeros_like(img)
        else:
            salida = (img - mn) / (mx - mn) * 255.0
    else:
        raise ValueError("modo debe ser 'clip' o 'norm'")
    return np.round(salida).astype(np.uint8)


# ---------------------------------------------------------------------------
# Parte 1: transformaciones lineales
# ---------------------------------------------------------------------------
def lineal(img, a=1.0, b=0.0, modo="clip"):
    """I' = a*I + b. Si modo=None devuelve el resultado flotante sin acotar."""
    salida = a * np.asarray(img, dtype=np.float64) + b
    return salida if modo is None else a_uint8(salida, modo)


def por_tramos(img, puntos):
    """
    Transformación lineal por tramos definida por puntos de control
    [(r0, s0), (r1, s1), ..., (rn, sn)] con r creciente. Entre puntos se
    interpola linealmente (equivale a una LUT de 256 entradas).
    """
    r, s = zip(*puntos)
    lut = np.interp(np.arange(256), r, s)
    return a_uint8(lut, "clip")[np.asarray(img, dtype=np.uint8)]


def inversion(img):
    """Negativo de la imagen: I' = 255 - I."""
    return (255 - np.asarray(img, dtype=np.int16)).astype(np.uint8)


# ---------------------------------------------------------------------------
# Parte 2: transformaciones no lineales (gamma)
# ---------------------------------------------------------------------------
def gamma(img, g, c=1.0, modo="clip"):
    """
    Corrección gamma sobre intensidades normalizadas a [0, 1]:
        I' = 255 * c * (I / 255) ** g
    Con c = 1 el resultado ya queda en [0, 255] (0 -> 0, 255 -> 255).
    """
    norm = np.asarray(img, dtype=np.float64) / 255.0
    salida = 255.0 * c * np.power(norm, g)
    return a_uint8(salida, modo)


def curva_gamma(g, c=1.0):
    """LUT (256 valores flotantes) de la transformación gamma."""
    return 255.0 * c * (np.arange(256) / 255.0) ** g


def ajuste_lineal_a_gamma(g, c=1.0):
    """
    Recta s = a*r + b que mejor aproxima (mínimos cuadrados) la curva gamma
    en todo el rango [0, 255]. Devuelve (a, b, error_rms).
    """
    r = np.arange(256, dtype=np.float64)
    s = curva_gamma(g, c)
    a, b = np.polyfit(r, s, 1)
    rms = np.sqrt(np.mean((a * r + b - s) ** 2))
    return a, b, rms


# ---------------------------------------------------------------------------
# Parte 3: transformaciones en RGB
# ---------------------------------------------------------------------------
def lineal_canales(img, a=(1, 1, 1), b=(0, 0, 0), modo="clip"):
    """Aplica X' = a_X * X + b_X de forma independiente a cada canal R, G, B."""
    img = np.asarray(img, dtype=np.float64)
    a = np.asarray(a, dtype=np.float64).reshape(1, 1, 3)
    b = np.asarray(b, dtype=np.float64).reshape(1, 1, 3)
    return a_uint8(a * img + b, modo)


def gamma_canales(img, gammas=(1, 1, 1)):
    """Aplica una gamma distinta a cada canal: X' = 255 * (X/255) ** g_X."""
    salida = np.empty_like(img)
    for k, g in enumerate(gammas):
        salida[..., k] = gamma(img[..., k], g)
    return salida


def eliminar_canal(img, canal):
    """Fija en cero el canal indicado ('R', 'G' o 'B')."""
    salida = img.copy()
    salida[..., "RGB".index(canal.upper())] = 0
    return salida


def intercambiar_canales(img, c1, c2):
    """Intercambia dos canales, p. ej. intercambiar_canales(img, 'R', 'B')."""
    i, j = "RGB".index(c1.upper()), "RGB".index(c2.upper())
    orden = [0, 1, 2]
    orden[i], orden[j] = orden[j], orden[i]
    return img[..., orden]


def a_gris(img_rgb):
    """Luminancia BT.601 (la misma que usa OpenCV): Y = 0.299R + 0.587G + 0.114B."""
    return cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)


# ---------------------------------------------------------------------------
# Métricas de apoyo para la interpretación
# ---------------------------------------------------------------------------
def estadisticas(img):
    """
    Resumen numérico de una imagen (por canal si es RGB): media, desviación
    estándar (medida de contraste global), mínimo, máximo, porcentaje de
    píxeles saturados en 0 y en 255, y número de niveles distintos usados.
    """
    img = np.asarray(img)
    canales = [("I", img)] if img.ndim == 2 else [(n, img[..., k]) for k, n in enumerate("RGB")]
    filas = []
    for nombre, ch in canales:
        filas.append({
            "canal": nombre,
            "media": float(ch.mean()),
            "desv": float(ch.std()),
            "min": int(ch.min()),
            "max": int(ch.max()),
            "%en0": 100.0 * float((ch == 0).mean()),
            "%en255": 100.0 * float((ch == 255).mean()),
            "niveles": int(np.unique(ch).size),
        })
    return filas


def detalle_en_sombras(original, transformada, umbral=64):
    """
    Cuantifica cuánto detalle se recupera en las zonas oscuras de la imagen
    ORIGINAL (píxeles con intensidad < umbral):
      - niveles: niveles de gris distintos que ocupan esas zonas tras la
        transformación (más niveles = más gradaciones distinguibles).
      - desv:    desviación estándar local en esas zonas (contraste en sombras).
      - %sat255: porcentaje de TODA la imagen que quedó saturada en 255.
    """
    o = np.asarray(original)
    t = np.asarray(transformada)
    if o.ndim == 3:
        o, t = a_gris(o), a_gris(t)
    mascara = o < umbral
    return {
        "niveles": int(np.unique(t[mascara]).size),
        "desv": float(t[mascara].std()),
        "%sat255": 100.0 * float((t == 255).mean()),
    }
