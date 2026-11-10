"""Limpieza de la tabla empresas (HU L01).

Uso:
    python scripts/limpiar_empresas.py empresas_sucio.csv

Lee el CSV sucio, imprime el diagnostico, corrige los errores,
imprime el diagnostico otra vez y guarda empresas_limpio.csv
en la misma carpeta del archivo de entrada.
"""
import sys
from pathlib import Path

import pandas as pd

# Columnas que no pueden quedar con nulos despues de limpiar.
# "contacto" no esta aqui porque se rellena con "Sin contacto".
COLUMNAS_OBLIGATORIAS = ["nombre", "nit", "sector", "telefono", "activa"]


def leer_csv(ruta):
    """Lee el CSV como texto para no perder ceros iniciales en nit y telefono."""
    return pd.read_csv(ruta, dtype=str, encoding="utf-8")


def diagnostico(df, titulo):
    """Imprime shape, info, nulos por columna y duplicados exactos."""
    print(f"\n===== {titulo} =====")
    print("shape:", df.shape)
    print("\ninfo:")
    df.info()
    print("\nnulos por columna:")
    print(df.isna().sum())
    print("\nduplicados exactos:", df.duplicated().sum())


def vacios_a_nulo(df):
    """Convierte textos vacios o solo espacios en nulos reales (NaN)."""
    return df.replace(r"^\s*$", pd.NA, regex=True)


def limpiar_texto(df):
    """Quita espacios sobrantes en nombre y unifica el sector (Title Case)."""
    df["nombre"] = df["nombre"].str.strip()
    df["sector"] = df["sector"].str.strip().str.title()
    return df


def limpiar_nit(df):
    """Deja el nit en un solo formato: sin puntos ni guiones."""
    df["nit"] = df["nit"].str.strip().str.replace(r"[.\-]", "", regex=True)
    return df


def limpiar_telefono(df):
    """Deja el telefono solo con digitos; si no queda ninguno, lo marca nulo."""
    df["telefono"] = df["telefono"].str.replace(r"\D", "", regex=True)
    df["telefono"] = df["telefono"].replace("", pd.NA)
    return df


def convertir_activa(df):
    """Convierte activa (texto) a booleano real; valores desconocidos quedan nulos."""
    df["activa"] = (
        df["activa"].astype(str).str.strip().str.upper()
        .map({"TRUE": True, "SI": True, "1": True,
              "FALSE": False, "NO": False, "0": False})
    )
    return df


def rellenar_contacto(df):
    """Rellena los contactos vacios con 'Sin contacto'."""
    df["contacto"] = df["contacto"].str.strip().fillna("Sin contacto")
    return df


def marcar_correos(df):
    """Crea la columna correo_valido (True si el correo contiene '@')."""
    df["correo"] = df["correo"].str.strip()
    df["correo_valido"] = df["correo"].str.contains("@", na=False)
    return df


def limpiar(df):
    """Aplica todas las correcciones en orden y devuelve el DataFrame limpio."""
    df = df.drop_duplicates()          # duplicados exactos del archivo original
    df = vacios_a_nulo(df)
    df = limpiar_texto(df)
    df = limpiar_nit(df)
    df = limpiar_telefono(df)
    df = convertir_activa(df)
    df = rellenar_contacto(df)
    df = marcar_correos(df)
    # Filas sin datos obligatorios no se pueden usar: se eliminan.
    df = df.dropna(subset=COLUMNAS_OBLIGATORIAS)
    # La limpieza puede crear duplicados nuevos (ej. 'Acme' y ' Acme '):
    df = df.drop_duplicates()
    return df.reset_index(drop=True)


def main():
    """Punto de entrada: lee, diagnostica, limpia, diagnostica y guarda."""
    if len(sys.argv) != 2:
        print("Uso: python scripts/limpiar_empresas.py empresas_sucio.csv")
        sys.exit(1)

    ruta_entrada = Path(sys.argv[1])
    if not ruta_entrada.exists():
        print(f"No se encontro el archivo: {ruta_entrada}")
        sys.exit(1)

    df = leer_csv(ruta_entrada)
    filas_antes = len(df)
    diagnostico(df, "DIAGNOSTICO ANTES DE LIMPIAR")

    df = limpiar(df)
    diagnostico(df, "DIAGNOSTICO DESPUES DE LIMPIAR")

    print(f"\nFilas antes: {filas_antes} | despues: {len(df)} "
          f"| eliminadas: {filas_antes - len(df)}")

    ruta_salida = ruta_entrada.with_name("empresas_limpio.csv")
    df.to_csv(ruta_salida, index=False, encoding="utf-8")
    print(f"Archivo guardado en: {ruta_salida}")


if __name__ == "__main__":
    main()