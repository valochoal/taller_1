"""
Funciones de visualización: imágenes lado a lado con sus histogramas,
curvas de transferencia y tablas de estadísticas.
"""

import matplotlib.pyplot as plt
import numpy as np

from .transformaciones import estadisticas

# El color de cada histograma identifica el canal que representa.
COLOR_CANAL = {"R": "#d62728", "G": "#2ca02c", "B": "#1f77b4", "I": "#444444"}
TINTA = "#333333"
GRILLA = "#dddddd"


def _estilo_ejes(ax):
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color("#999999")
    ax.tick_params(colors=TINTA, labelsize=8)
    ax.grid(axis="y", color=GRILLA, linewidth=0.6)
    ax.set_axisbelow(True)


def histograma(ax, img, titulo=None, log=False):
    """Histograma de 256 bins; en RGB se dibuja una curva por canal."""
    img = np.asarray(img)
    x = np.arange(256)
    canales = [("I", img)] if img.ndim == 2 else [(n, img[..., k]) for k, n in enumerate("RGB")]
    hists = {n: np.bincount(ch.ravel(), minlength=256) for n, ch in canales}
    for n, h in hists.items():
        if n == "I":
            ax.fill_between(x, h, step="mid", color=COLOR_CANAL["I"], alpha=0.35, linewidth=0)
            ax.plot(x, h, drawstyle="steps-mid", color=COLOR_CANAL["I"], linewidth=1)
        else:
            ax.plot(x, h, color=COLOR_CANAL[n], linewidth=1.2, label=n)
    if img.ndim == 3:
        ax.legend(fontsize=7, frameon=False, loc="upper center", ncol=3)
    ax.set_xlim(-2, 257)
    if log:
        ax.set_yscale("log")
    else:
        # Los picos de saturación en 0 y 255 pueden aplastar el resto del
        # histograma: se limita el eje y a los valores interiores y se
        # indica con texto el porcentaje de píxeles en cada extremo.
        interior = max(h[1:255].max() for h in hists.values())
        tope = max(interior, 1) * 1.15
        ax.set_ylim(0, tope)
        total = img.shape[0] * img.shape[1]
        p0 = max(h[0] for h in hists.values()) / total * 100
        p255 = max(h[255] for h in hists.values()) / total * 100
        if max(h[0] for h in hists.values()) > tope:
            ax.text(3, tope * 0.93, f"◄ {p0:.1f}% en 0", fontsize=7, color=TINTA, va="top")
        if max(h[255] for h in hists.values()) > tope:
            ax.text(252, tope * 0.93, f"{p255:.1f}% en 255 ►", fontsize=7, color=TINTA, va="top", ha="right")
    ax.set_xlabel("Intensidad", fontsize=8, color=TINTA)
    ax.set_yticklabels([])
    if titulo:
        ax.set_title(titulo, fontsize=9, color=TINTA)
    _estilo_ejes(ax)


def comparar(imagenes, titulo=None, log=False, ancho=4.0):
    """
    Muestra una fila de imágenes y, debajo de cada una, su histograma.

    imagenes: lista de tuplas (titulo, imagen). La primera suele ser la original.
    """
    n = len(imagenes)
    fig, ejes = plt.subplots(2, n, figsize=(ancho * n, ancho * 1.35),
                             gridspec_kw={"height_ratios": [3, 1.3]}, squeeze=False)
    for j, (t, img) in enumerate(imagenes):
        ax = ejes[0, j]
        if np.asarray(img).ndim == 2:
            ax.imshow(img, cmap="gray", vmin=0, vmax=255)
        else:
            ax.imshow(img)
        ax.set_title(t, fontsize=10, color=TINTA)
        ax.axis("off")
        histograma(ejes[1, j], img, log=log)
    if titulo:
        fig.suptitle(titulo, fontsize=12, color=TINTA, fontweight="bold")
    fig.tight_layout()
    plt.show()


def curvas(curvas_dict, titulo="Curvas de transferencia", identidad=True, ax=None):
    """
    Grafica funciones de transferencia s = T(r) para r en [0, 255].
    curvas_dict: {etiqueta: arreglo de 256 valores (o función de r)}.
    """
    r = np.arange(256)
    propio = ax is None
    if propio:
        fig, ax = plt.subplots(figsize=(4.6, 4.2))
    if identidad:
        ax.plot(r, r, color="#999999", linestyle="--", linewidth=1, label="identidad")
    for etiqueta, curva in curvas_dict.items():
        valores = curva(r) if callable(curva) else np.asarray(curva)
        ax.plot(r, valores, linewidth=2, label=etiqueta)
    ax.axhspan(255, max(260, ax.get_ylim()[1]), color="#f2dede", alpha=0.6, linewidth=0)
    ax.axhspan(min(-5, ax.get_ylim()[0]), 0, color="#f2dede", alpha=0.6, linewidth=0)
    ax.set_xlim(0, 255)
    ax.set_xlabel("Entrada r", fontsize=9, color=TINTA)
    ax.set_ylabel("Salida s", fontsize=9, color=TINTA)
    ax.set_title(titulo, fontsize=10, color=TINTA)
    ax.legend(fontsize=7, frameon=False)
    _estilo_ejes(ax)
    ax.grid(color=GRILLA, linewidth=0.6)
    if propio:
        fig.tight_layout()
        plt.show()


def tabla(imagenes, decimales=1):
    """Imprime una tabla de estadísticas para una lista de (titulo, imagen)."""
    encabezado = f"{'imagen':<32}{'canal':>6}{'media':>8}{'desv':>8}{'min':>5}{'max':>5}{'%en0':>7}{'%en255':>8}{'niveles':>9}"
    print(encabezado)
    print("-" * len(encabezado))
    for t, img in imagenes:
        for fila in estadisticas(img):
            print(f"{t[:31]:<32}{fila['canal']:>6}{fila['media']:>8.{decimales}f}"
                  f"{fila['desv']:>8.{decimales}f}{fila['min']:>5}{fila['max']:>5}"
                  f"{fila['%en0']:>7.2f}{fila['%en255']:>8.2f}{fila['niveles']:>9}")
