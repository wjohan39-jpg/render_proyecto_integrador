"""
HU G01 - Reporte gráfico de la tabla prioridades (proyecto integrador).

Uso (desde la raiz del proyecto, sin argumentos):
    python main.py
o directamente:
    python src/notebook/graficacion/graficar.py [ruta_limpio]

Por defecto lee `data/limpio/prioridades_limpio.csv`.

Lee el CSV limpio, crea tres gráficas con matplotlib, las guarda en
reportes/ (dpi=120) e imprime la ruta de cada una y las conclusiones.
"""

import os
import sys

import matplotlib

# Backend sin ventana: el script guarda las imágenes y no se queda esperando.
matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.ticker import MaxNLocator  # noqa: E402

RUTA_POR_DEFECTO = os.path.join("data", "limpio", "prioridades_limpio.csv")
CARPETA_SALIDA = "reportes"
NIVEL_MIN = 1
NIVEL_MAX = 5
PRIORIDADES_ESPERADAS = 5


def encontrar_columna(df, candidatos, contiene=None):
    """Busca en el DataFrame la columna que corresponde a un campo.

    Prueba primero los nombres exactos de `candidatos` y, si no aparece
    ninguno, la primera columna cuyo nombre contenga el texto `contiene`.
    Si no encuentra nada, detiene el script con un mensaje claro.
    """
    columnas = {str(c).strip().lower(): c for c in df.columns}
    for nombre in candidatos:
        if nombre in columnas:
            return columnas[nombre]
    if contiene:
        for clave, original in columnas.items():
            if contiene in clave:
                return original
    sys.exit(
        f"Error: no encontré la columna {candidatos[0]!r} en el archivo. "
        f"Columnas disponibles: {list(df.columns)}"
    )


def leer_datos(ruta_csv):
    """Lee prioridades_limpio.csv y deja las columnas listas para graficar.

    Devuelve el DataFrame con tres columnas estándar: `nombre` (texto sin
    espacios sobrantes), `nivel` (número) y `dias` (número).
    """
    if not os.path.isfile(ruta_csv):
        sys.exit(f"Error: no existe el archivo {ruta_csv!r}.")

    df = pd.read_csv(ruta_csv, encoding="utf-8")
    col_nombre = encontrar_columna(
        df, ["nombre", "prioridad", "descripcion"], contiene="prioridad"
    )
    col_nivel = encontrar_columna(df, ["nivel"], contiene="nivel")
    col_dias = encontrar_columna(
        df,
        ["dias_max_respuesta", "dias_maximos_respuesta", "dias_max", "dias"],
        contiene="dia",
    )

    datos = pd.DataFrame(
        {
            "nombre": df[col_nombre].astype(str).str.strip().str.capitalize(),
            "nivel": pd.to_numeric(df[col_nivel], errors="coerce"),
            "dias": pd.to_numeric(df[col_dias], errors="coerce"),
        }
    )
    # Una fila sin nivel o sin días no se puede graficar.
    return datos.dropna(subset=["nivel", "dias"]).reset_index(drop=True)


def nivel_como_texto(valor):
    """Muestra el nivel sin decimales cuando es un número entero (3.0 -> 3)."""
    return int(valor) if float(valor).is_integer() else valor


def orden_de_prioridades(df):
    """Devuelve los nombres de prioridad ordenados por su nivel (menor a mayor)."""
    return df.groupby("nombre")["nivel"].min().sort_values().index


def guardar_grafica(numero):
    """Cierra la gráfica actual: ajusta el diseño, la guarda y la cierra.

    Devuelve la ruta del PNG creado (reportes/prioridades_grafica_N.png).
    """
    os.makedirs(CARPETA_SALIDA, exist_ok=True)
    ruta = os.path.join(CARPETA_SALIDA, f"prioridades_grafica_{numero}.png")
    plt.tight_layout()
    plt.savefig(ruta, dpi=120)
    plt.close()
    return ruta


def grafica_1_filas_por_nivel(df):
    """Gráfica 1 (barras): cuántas filas hay por nivel."""
    por_nivel = df["nivel"].value_counts().sort_index()
    por_nivel.index = [nivel_como_texto(n) for n in por_nivel.index]

    ax = por_nivel.plot(kind="bar", figsize=(7, 5), color="#4C78A8")
    ax.bar_label(ax.containers[0])
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))  # solo enteros
    plt.title("Cantidad de filas por nivel")
    plt.xlabel("Nivel")
    plt.ylabel("Número de filas")
    plt.xticks(rotation=0)
    return guardar_grafica(1)


def grafica_2_dias_promedio(df):
    """Gráfica 2 (barras): días promedio de respuesta por prioridad."""
    resumen = df.groupby("nombre")["dias"].agg(["mean", "min", "max", "count"])
    resumen = resumen.loc[orden_de_prioridades(df)]

    ax = resumen["mean"].plot(kind="bar", figsize=(7, 5), color="#F58518")
    ax.bar_label(ax.containers[0], fmt="%.1f")
    plt.title("Días promedio de respuesta por prioridad")
    plt.xlabel("Prioridad")
    plt.ylabel("Días promedio de respuesta")
    plt.xticks(rotation=30, ha="right")
    return guardar_grafica(2)


def grafica_3_reparto_prioridades(df):
    """Gráfica 3 (torta): reparto de las filas entre las prioridades."""
    conteo = df["nombre"].value_counts().reindex(orden_de_prioridades(df))

    conteo.plot(kind="pie", autopct="%1.1f%%", figsize=(6, 6))
    plt.title("Reparto de las prioridades")
    plt.xlabel("Prioridad")
    plt.ylabel("Porcentaje de filas", labelpad=25)  # separa el titulo de las etiquetas
    return guardar_grafica(3)


def conclusion_prioridades_reales(df):
    """Responde cuántas prioridades reales quedaron al final.

    Una prioridad es real si su nivel está entre 1 y 5; el resultado se
    calcula con los datos y se compara con las 5 esperadas.
    """
    validas = df[df["nivel"].between(NIVEL_MIN, NIVEL_MAX)]
    reales = validas["nombre"].nunique()
    total = df["nombre"].nunique()

    texto = (
        f"1. Prioridades reales: quedaron {reales} "
        f"(con nivel entre {NIVEL_MIN} y {NIVEL_MAX}); "
        f"el archivo tiene {total} nombres distintos en total. "
    )
    if reales == PRIORIDADES_ESPERADAS and total == reales:
        texto += f"Coincide con las {PRIORIDADES_ESPERADAS} esperadas: la limpieza quedó bien."
    else:
        texto += (
            f"No coincide con las {PRIORIDADES_ESPERADAS} esperadas: "
            "revisa la limpieza (nombres repetidos o niveles inventados)."
        )
    return texto


def conclusion_nivel_y_dias(df):
    """Explica la relación entre el nivel y los días máximos de respuesta.

    Usa el promedio de días por nivel y la correlación entre ambas columnas.
    """
    por_nivel = df.groupby("nivel")["dias"].mean().sort_index()
    detalle = ", ".join(
        f"nivel {nivel_como_texto(n)}: {d:.1f} días" for n, d in por_nivel.items()
    )
    correlacion = df["nivel"].corr(df["dias"])

    if pd.isna(correlacion) or abs(correlacion) < 0.3:
        relacion = "no se ve una relación clara entre el nivel y los días"
    elif correlacion > 0:
        relacion = "a mayor nivel, más días máximos de respuesta (relación directa)"
    else:
        relacion = "a mayor nivel, menos días máximos de respuesta (relación inversa)"

    texto = f"2. Nivel y días máximos de respuesta: {relacion}. "
    if not pd.isna(correlacion):
        texto += f"La correlación es {correlacion:.2f}. "
    return texto + f"Promedios: {detalle}."


def conclusion_validar_nivel(df):
    """Explica por qué el back debe validar que nivel esté entre 1 y 5.

    Agrega cuántas filas del archivo están fuera de ese rango.
    """
    fuera = int((~df["nivel"].between(NIVEL_MIN, NIVEL_MAX)).sum())
    return (
        f"3. Validación del nivel en el back: hoy hay {fuera} fila(s) con nivel "
        f"fuera de {NIVEL_MIN}-{NIVEL_MAX}. El back debe validarlo porque "
        f"(a) los {NIVEL_MAX} niveles son un catálogo cerrado y cualquier otro "
        "valor crea una prioridad falsa; (b) el front se puede saltar (Postman, "
        "otro cliente, un error de código), así que el back es la última barrera "
        "antes de la base de datos; (c) un nivel inválido distorsiona las "
        "gráficas, los promedios y la relación nivel-días; y (d) es más barato "
        "rechazar el dato al entrar que limpiarlo después."
    )


def imprimir_conclusiones(df):
    """Imprime las conclusiones que pide la HU, una por pregunta."""
    print("\nCONCLUSIONES")
    print(conclusion_prioridades_reales(df))
    print(conclusion_nivel_y_dias(df))
    print(conclusion_validar_nivel(df))


def main():
    """Lee el CSV, crea las tres gráficas e imprime rutas y conclusiones."""
    ruta = sys.argv[1] if len(sys.argv) > 1 else RUTA_POR_DEFECTO

    df = leer_datos(ruta)
    if df.empty:
        sys.exit("Error: el archivo no tiene filas con nivel y días válidos.")

    print(f"Filas leídas: {len(df)}\n")
    print("GRÁFICAS GUARDADAS")
    for ruta_png in (
        grafica_1_filas_por_nivel(df),
        grafica_2_dias_promedio(df),
        grafica_3_reparto_prioridades(df),
    ):
        print(ruta_png)

    imprimir_conclusiones(df)


if __name__ == "__main__":
    main()