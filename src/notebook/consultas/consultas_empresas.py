"""Consultas HU Q01 sobre la tabla empresas (archivo LIMPIO).

Uso:
    python scripts/consultas_empresas.py empresas_limpio.csv

Resuelve cinco consultas con pandas, imprime el titulo y el resultado de
cada una y guarda empresas_consulta_N.csv junto al archivo de entrada.
"""
import os
import sys

import pandas as pd


def cargar_datos(ruta):
    """Lee el CSV limpio y se asegura de que 'activa' sea booleana."""
    df = pd.read_csv(ruta)
    if df["activa"].dtype != bool:
        # Por si el CSV trae textos como "True"/"False"/"Si"/"No"
        df["activa"] = (
            df["activa"].astype(str).str.strip().str.lower()
            .isin(["true", "1", "si", "sí", "verdadero"])
        )
    return df


def consulta_1_activas(df):
    """Consulta 1: devuelve las empresas activas."""
    print("\n=== Consulta 1: ¿Qué empresas están activas? ===")
    activas = df[df["activa"] == True]
    print(activas.to_string(index=False))
    return activas


def consulta_2_sector_ordenado(df, sector="Tecnologia"):
    """Consulta 2: empresas de un sector, ordenadas por nombre."""
    print(f"\n=== Consulta 2: ¿Qué empresas son del sector {sector}, ordenadas por nombre? ===")
    logistica = df[df["sector"] == sector].sort_values("nombre")
    print(logistica.to_string(index=False))
    return logistica


def consulta_3_conteo_sector(df):
    """Consulta 3: conteo rápido de empresas por sector (value_counts)."""
    print("\n=== Consulta 3: ¿Cuántas empresas hay por sector (conteo rápido)? ===")
    conteo = df["sector"].value_counts()
    print(conteo.to_string())
    # Se convierte a DataFrame para que el CSV tenga encabezados claros
    return conteo.rename_axis("sector").reset_index(name="cantidad")


def consulta_4_groupby_sector(df):
    """Consulta 4 (groupby): empresas por sector, de mayor a menor."""
    print("\n=== Consulta 4: ¿Cuántas empresas hay por sector, de mayor a menor? (groupby) ===")
    por_sector = df.groupby("sector")["id"].count().sort_values(ascending=False)
    print(por_sector.to_string())
    return por_sector.rename("cantidad").reset_index()


def consulta_5_groupby_doble(df):
    """Consulta 5 (groupby doble): activas e inactivas por sector."""
    print("\n=== Consulta 5: ¿Cuántas empresas activas e inactivas hay por sector? (groupby doble) ===")
    tabla = df.groupby(["sector", "activa"])["id"].count().unstack(fill_value=0)
    print(tabla.to_string())
    return tabla.reset_index()


def main():
    """Lee el archivo, ejecuta las cinco consultas en orden y guarda los CSV."""
    if len(sys.argv) != 2:
        print("Uso: python scripts/consultas_empresas.py empresas_limpio.csv")
        sys.exit(1)

    ruta = sys.argv[1]
    carpeta = os.path.dirname(os.path.abspath(ruta))
    df = cargar_datos(ruta)

    funciones = [
        consulta_1_activas,
        consulta_2_sector_ordenado,
        consulta_3_conteo_sector,
        consulta_4_groupby_sector,
        consulta_5_groupby_doble,
    ]
    for n, funcion in enumerate(funciones, start=1):
        resultado = funcion(df)
        salida = os.path.join(carpeta, f"empresas_consulta_{n}.csv")
        resultado.to_csv(salida, index=False)
        print(f"-> Guardado: {salida}")


if __name__ == "__main__":
    main()