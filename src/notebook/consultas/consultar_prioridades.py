"""Consultas de la HU Q01 sobre la tabla prioridades del proyecto integrador.

Uso:
    python scripts/consultas_prioridades.py prioridades_limpio.csv

Lee el archivo LIMPIO (no el sucio), resuelve las cinco consultas con pandas,
imprime el título y el resultado de cada una, en orden, y guarda cada
resultado como prioridades_consulta_N.csv en la misma carpeta del archivo leído.
"""

import sys
from pathlib import Path

import pandas as pd

# Ruta que se usa si no se pasa ningún archivo al ejecutar el script.
RUTA_POR_DEFECTO = "data/limpio/prioridades_limpio.csv"

# Columnas que necesitan las consultas.
COLUMNAS = ["id", "nombre", "nivel", "dias_max_respuesta"]


def leer_datos(ruta):
    """Lee prioridades_limpio.csv y revisa que sea el archivo limpio:
    que existan las columnas necesarias y que nivel y dias_max_respuesta
    sean números. Si algo falla, avisa en español y termina."""
    if not ruta.exists():
        sys.exit(f"No encuentro el archivo: {ruta}")

    df = pd.read_csv(ruta)

    faltan = [c for c in COLUMNAS if c not in df.columns]
    if faltan:
        sys.exit(f"Al archivo le faltan las columnas: {', '.join(faltan)}")

    for columna in ["nivel", "dias_max_respuesta"]:
        if not pd.api.types.is_numeric_dtype(df[columna]):
            sys.exit(
                f"La columna '{columna}' no es numérica. "
                "¿Estás usando el archivo sucio en vez de prioridades_limpio.csv?"
            )
    return df


def mostrar_y_guardar(resultado, numero, carpeta):
    """Imprime el resultado de una consulta y lo guarda como
    prioridades_consulta_N.csv en la carpeta indicada."""
    print(resultado.to_string(index=False))
    print()
    resultado.to_csv(carpeta / f"prioridades_consulta_{numero}.csv", index=False)


def consulta_1(df, carpeta):
    """Consulta 1: prioridades ordenadas de la más urgente (nivel 1)
    a la menos urgente. Usa kind='stable' para que las filas con el mismo
    nivel conserven su orden original."""
    print("Consulta 1 - ¿Cuáles son las prioridades, de la más urgente a la menos urgente?")
    ordenadas = df.sort_values("nivel", kind="stable")
    mostrar_y_guardar(ordenadas, 1, carpeta)
    return ordenadas


def consulta_2(df, carpeta):
    """Consulta 2: solo las prioridades urgentes (nivel 1 y 2)."""
    print("Consulta 2 - ¿Cuáles son solo las prioridades urgentes (nivel 1 y 2)?")
    urgentes = df[df["nivel"] <= 2]
    mostrar_y_guardar(urgentes, 2, carpeta)
    return urgentes


def consulta_3(df, carpeta):
    """Consulta 3: cuántas veces aparece cada nombre. Sirve para detectar
    variantes del mismo nombre (mayúsculas, tildes, espacios)."""
    print("Consulta 3 - ¿Cuántas veces aparece cada nombre? (sirve para detectar variantes)")
    conteo = df["nombre"].value_counts()
    # Se convierte en tabla de dos columnas para guardarla y mostrarla clara.
    resultado = conteo.rename_axis("nombre").reset_index(name="cantidad")
    mostrar_y_guardar(resultado, 3, carpeta)
    return resultado


def consulta_4(df, carpeta):
    """Consulta 4 (GROUPBY): cuántas filas hay por nivel."""
    print("Consulta 4 - ¿Cuántas filas hay por nivel? (groupby)")
    por_nivel = df.groupby("nivel")["id"].count()
    resultado = por_nivel.reset_index(name="cantidad")
    mostrar_y_guardar(resultado, 4, carpeta)
    return resultado


def consulta_5(df, carpeta):
    """Consulta 5 (GROUPBY): días de respuesta mínimo, promedio y máximo
    por prioridad (por nombre), con un decimal."""
    print("Consulta 5 - ¿Cuáles son los días de respuesta mínimo, promedio y máximo por prioridad? (groupby)")
    resumen = df.groupby("nombre")["dias_max_respuesta"].agg(["min", "mean", "max"]).round(1)
    resultado = resumen.reset_index()
    mostrar_y_guardar(resultado, 5, carpeta)
    return resultado


def main():
    """Lee el archivo limpio y ejecuta las cinco consultas en orden."""
    ruta = Path(sys.argv[1] if len(sys.argv) > 1 else RUTA_POR_DEFECTO)
    carpeta = ruta.parent  # Los resultados se guardan junto al archivo leído.
    df = leer_datos(ruta)

    for consulta in (consulta_1, consulta_2, consulta_3, consulta_4, consulta_5):
        consulta(df, carpeta)


if __name__ == "__main__":
    main()