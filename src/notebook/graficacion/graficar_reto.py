"""Gráficas y conclusiones de la tabla retos del proyecto integrador (HU G01 de Kaizen).

Uso:
    python src/notebook/graficacion/graficar_reto.py

Lee data/limpio/retos_limpio.csv, crea las tres gráficas en reportes/ y al final
imprime las conclusiones.
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Guarda las imágenes sin abrir ventanas
import matplotlib.pyplot as plt
import pandas as pd

# Raíz del proyecto: integrador_diego_zea/ (este archivo está en src/notebook/graficacion/)
RAIZ = Path(__file__).resolve().parents[3]

RUTA_ENTRADA = RAIZ / "data" / "limpio" / "retos_limpio.csv"
CARPETA_REPORTES = RAIZ / "reportes"


def cargar_datos(ruta_csv):
    """Lee el CSV limpio y convierte las fechas; agrega mes_inicio (AAAA-MM)."""
    if not ruta_csv.exists():
        sys.exit(f"ERROR: no se encontró '{ruta_csv}'. Ejecuta antes la limpieza.")
    df = pd.read_csv(ruta_csv)
    df["fecha_inicio"] = pd.to_datetime(df["fecha_inicio"])
    df["fecha_fin"] = pd.to_datetime(df["fecha_fin"])
    df["mes_inicio"] = df["fecha_inicio"].dt.to_period("M").astype(str)
    return df


def guardar_grafica(ruta):
    """Ajusta el diseño, guarda la imagen con dpi=120 y cierra la figura."""
    plt.tight_layout()
    plt.savefig(ruta, dpi=120)
    plt.close()
    print(f"Gráfica guardada en: {ruta}")


def grafica_1_barras_estado(df):
    """Gráfica 1 — Barras: cantidad de retos por estado."""
    plt.figure()
    conteo = df["estado"].value_counts()
    conteo.plot(kind="bar", color="skyblue", edgecolor="black")
    plt.title("Cantidad de retos por estado")
    plt.xlabel("Estado")
    plt.ylabel("Número de retos")
    plt.xticks(rotation=0)
    guardar_grafica(CARPETA_REPORTES / "retos_grafica_1.png")


def grafica_2_linea_mes(df):
    """Gráfica 2 — Línea: retos que empiezan cada mes."""
    plt.figure(figsize=(9, 5))
    por_mes = df["mes_inicio"].value_counts().sort_index()
    por_mes.plot(kind="line", marker="o", color="orange", linewidth=2)
    plt.title("Retos que empiezan cada mes")
    plt.xlabel("Mes de inicio")
    plt.ylabel("Número de retos")
    plt.xticks(range(len(por_mes)), por_mes.index, rotation=45)
    guardar_grafica(CARPETA_REPORTES / "retos_grafica_2.png")


def grafica_3_histograma_duracion(df):
    """Gráfica 3 — Histograma: cómo se reparte la duración de los retos."""
    plt.figure()
    df["duracion_dias"].plot(kind="hist", bins=20, color="green", edgecolor="black")
    plt.title("Distribución de la duración de los retos")
    plt.xlabel("Duración (días)")
    plt.ylabel("Frecuencia")
    guardar_grafica(CARPETA_REPORTES / "retos_grafica_3.png")


def imprimir_conclusiones(df):
    """Responde las preguntas de la HU con los datos."""
    print("\n--- Conclusiones ---")

    # 1. Mes donde se concentran los retos
    por_mes = df["mes_inicio"].value_counts()
    mes_pico = por_mes.idxmax()
    print(
        f"1. Concentración: el mes con más retos es {mes_pico} ({por_mes.max()} retos). "
        "Una posible causa es que algunos meses coincidan con el arranque de ciclos "
        "o cohortes; con datos simulados esto es solo una hipótesis."
    )

    # 2. Duración promedio según el estado
    print("2. Duración promedio por estado:")
    for estado, promedio in df.groupby("estado")["duracion_dias"].mean().items():
        print(f"   - {estado}: {promedio:.1f} días")

    # 3. Retos con fecha_fin antes de fecha_inicio (dato para el back)
    incoherentes = int((df["fecha_fin"] < df["fecha_inicio"]).sum())
    porcentaje = incoherentes / len(df) * 100 if len(df) else 0
    print(
        f"3. Para el back: {incoherentes} retos ({porcentaje:.1f}%) tenían la fecha de fin "
        "antes que la de inicio; conviene validar esto al crear un reto."
    )


def graficar_retos():
    """Punto de entrada: crea las tres gráficas y imprime las conclusiones."""
    # Opcional: se puede pasar otra ruta de CSV como argumento.
    ruta = Path(sys.argv[1]) if len(sys.argv) > 1 else RUTA_ENTRADA
    df = cargar_datos(ruta)

    # La carpeta se crea sola si no existe
    CARPETA_REPORTES.mkdir(parents=True, exist_ok=True)

    grafica_1_barras_estado(df)
    grafica_2_linea_mes(df)
    grafica_3_histograma_duracion(df)
    imprimir_conclusiones(df)


if __name__ == "__main__":
    graficar_retos()