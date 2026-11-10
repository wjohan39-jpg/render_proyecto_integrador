"""Consultas de la tabla retos del proyecto integrador (HU Q01 de Kaizen).

Uso:
    python src/notebook/consulta/consultar_reto.py

Lee data/limpio/retos_limpio.csv (el archivo LIMPIO), resuelve las cinco consultas,
las imprime en orden y guarda cada resultado en data/limpio/retos_consulta_N.csv.
"""

import sys
from pathlib import Path

import pandas as pd


RAIZ = Path(__file__).resolve().parents[3]

# Carpeta del archivo limpio y de los resultados de las consultas.
CARPETA_LIMPIO = RAIZ / "data" / "limpio"
RUTA_ENTRADA = CARPETA_LIMPIO / "retos_limpio.csv"


def cargar_datos(ruta_archivo):
    """Lee el CSV limpio y convierte fecha_inicio y fecha_fin a datetime."""
    if not ruta_archivo.exists():
        sys.exit(f"ERROR: no se encontró '{ruta_archivo}'. Ejecuta antes la limpieza.")
    df = pd.read_csv(ruta_archivo)
    for columna in ["fecha_inicio", "fecha_fin"]:
        df[columna] = pd.to_datetime(df[columna])
    return df


def ruta_consulta(numero):
    """Devuelve la ruta data/limpio/retos_consulta_N.csv."""
    return CARPETA_LIMPIO / f"retos_consulta_{numero}.csv"


def consulta_1_en_curso(df):
    """Consulta 1 — Retos que están en curso: filtra estado == 'EN_CURSO'."""
    en_curso = df[df["estado"] == "EN_CURSO"]
    en_curso.to_csv(ruta_consulta(1), index=False, encoding="utf-8")
    return en_curso


def consulta_2_mas_largos(df):
    """Consulta 2 — Los 10 retos más largos, por duracion_dias."""
    largos = df.nlargest(10, "duracion_dias")[["nombre", "duracion_dias", "estado"]]
    largos.to_csv(ruta_consulta(2), index=False, encoding="utf-8")
    return largos


def consulta_3_conteo_estado(df):
    """Consulta 3 — Cuántos retos hay por estado, con value_counts()."""
    conteo = df["estado"].value_counts()
    conteo.to_csv(ruta_consulta(3), header=["conteo"], encoding="utf-8")
    return conteo


def consulta_4_resumen_groupby(df):
    """Consulta 4 — GROUPBY: duración promedio, mínima y máxima por estado."""
    resumen = df.groupby("estado")["duracion_dias"].agg(["count", "mean", "min", "max"])
    resumen.to_csv(ruta_consulta(4), encoding="utf-8")
    return resumen


def consulta_5_por_mes(df):
    """Consulta 5 — GROUPBY por mes: cuántos retos empiezan cada mes."""
    por_mes = df.groupby(df["fecha_inicio"].dt.to_period("M"))["id"].count()
    por_mes.to_csv(ruta_consulta(5), header=["conteo"], encoding="utf-8")
    return por_mes


def consultar_retos():
    """Punto de entrada: carga el CSV limpio y muestra las cinco consultas en orden."""
    # Opcional: se puede pasar otra ruta de CSV como argumento.
    ruta = Path(sys.argv[1]) if len(sys.argv) > 1 else RUTA_ENTRADA
    df = cargar_datos(ruta)

    print("=== CONSULTA 1: Retos en curso ===")
    print(consulta_1_en_curso(df))

    print("\n=== CONSULTA 2: Los 10 retos más largos ===")
    print(consulta_2_mas_largos(df))

    print("\n=== CONSULTA 3: Conteo de retos por estado ===")
    print(consulta_3_conteo_estado(df))

    print("\n=== CONSULTA 4: Duración (count, mean, min, max) por estado ===")
    print(consulta_4_resumen_groupby(df))

    print("\n=== CONSULTA 5: Retos que empiezan cada mes ===")
    print(consulta_5_por_mes(df))

    print(f"\nResultados guardados en: {CARPETA_LIMPIO}")


if __name__ == "__main__":
    consultar_retos()