"""Limpieza de la tabla retos del proyecto integrador (HU L01 de Kaizen).

Uso:
    python src/notebook/limpieza/limpiar_reto.py

Lee data/crudo/retos_sucio.csv, imprime el diagnóstico, corrige los errores que
piden los criterios, imprime el diagnóstico otra vez y guarda
data/limpio/retos_limpio.csv.
"""

import sys
from pathlib import Path

import pandas as pd

# Raíz del proyecto: integrador_diego_zea/ (este archivo está en src/notebook/limpieza/)
RAIZ = Path(__file__).resolve().parents[3]

# Rutas que pide la HU, siempre desde la raíz del proyecto.
RUTA_ENTRADA = RAIZ / "data" / "crudo" / "retos_sucio.csv"
RUTA_SALIDA = RAIZ / "data" / "limpio" / "retos_limpio.csv"

# Columnas que no pueden quedar con nulos después de limpiar.
# "descripcion" no está aquí porque se rellena con "Sin descripcion".
COLUMNAS_OBLIGATORIAS = ["id", "nombre", "estado", "fecha_inicio", "fecha_fin"]


def encontrar_archivo(argumento=None):
    """Devuelve la ruta del CSV sucio: la que se pasó o, si no, data/crudo/retos_sucio.csv."""
    ruta = Path(argumento) if argumento else RUTA_ENTRADA
    if not ruta.exists():
        sys.exit(f"ERROR: no se encontró el archivo '{ruta}'. Ejecuta antes la exportación.")
    return ruta


def leer_datos(ruta):
    """Lee el CSV con pd.read_csv() y devuelve el DataFrame."""
    try:
        return pd.read_csv(ruta)
    except Exception as error:  # archivo vacío, mal formado, etc.
        sys.exit(f"ERROR: no se pudo leer '{ruta}': {error}")


def imprimir_diagnostico(df, titulo):
    """Imprime shape, info, nulos por columna y cantidad de duplicados exactos."""
    print(f"\n{'=' * 60}\nDIAGNÓSTICO {titulo}\n{'=' * 60}")
    print(f"df.shape: {df.shape}")
    print("\ndf.info():")
    df.info()
    print("\ndf.isna().sum():")
    print(df.isna().sum())
    print(f"\ndf.duplicated().sum(): {df.duplicated().sum()}")


def quitar_duplicados(df):
    """Quita los duplicados exactos con drop_duplicates()."""
    return df.drop_duplicates()


def convertir_fechas(df):
    """Convierte fecha_inicio y fecha_fin a datetime aunque vengan en dos formatos.

    Primero lee las fechas ISO (AAAA-MM-DD) tal cual, porque dayfirst=True las
    confundiría (2026-03-05 sería 3 de mayo). Las demás (DD/MM/AAAA) se leen con
    format="mixed" y dayfirst=True. Lo que no se pueda interpretar queda como NaT.
    """
    for columna in ["fecha_inicio", "fecha_fin"]:
        texto = df[columna].astype("string").str.strip()
        iso = pd.to_datetime(texto, format="%Y-%m-%d", errors="coerce")
        resto = pd.to_datetime(texto, format="mixed", dayfirst=True, errors="coerce")
        df[columna] = iso.fillna(resto)
    return df


def unificar_estado(df):
    """Unifica el estado: sin espacios en los bordes, en MAYÚSCULAS y con guion bajo."""
    df["estado"] = (
        df["estado"]
        .astype("string")
        .str.strip()
        .str.upper()
        .str.replace(r"\s+", "_", regex=True)
    )
    return df


def rellenar_descripciones(df):
    """Rellena las descripciones vacías (nulas o solo espacios) con 'Sin descripcion'."""
    descripcion = df["descripcion"].astype("string")
    descripcion = descripcion.mask(descripcion.str.strip() == "")
    df["descripcion"] = descripcion.fillna("Sin descripcion")
    return df


def crear_duracion(df):
    """Crea duracion_dias = fecha_fin - fecha_inicio, en días."""
    df["duracion_dias"] = (df["fecha_fin"] - df["fecha_inicio"]).dt.days.astype("Int64")
    return df


def marcar_fechas_incoherentes(df):
    """Marca con fecha_valida=False las filas donde el fin es anterior al inicio.

    Devuelve el DataFrame y la cantidad de fechas incoherentes.
    """
    df["fecha_valida"] = df["duracion_dias"] >= 0
    incoherentes = int((df["duracion_dias"] < 0).sum())
    return df, incoherentes


def quitar_nulos_obligatorios(df):
    """Elimina las filas con nulos en las columnas obligatorias (ej. fecha ilegible)."""
    return df.dropna(subset=COLUMNAS_OBLIGATORIAS)


def limpiar(df):
    """Aplica todas las correcciones en orden y devuelve (df_limpio, incoherentes)."""
    df = quitar_duplicados(df)
    df = convertir_fechas(df)
    df = unificar_estado(df)
    df = rellenar_descripciones(df)
    df = crear_duracion(df)
    df, incoherentes = marcar_fechas_incoherentes(df)
    df = quitar_nulos_obligatorios(df)
    # Al normalizar pueden aparecer duplicados nuevos: se vuelven a quitar.
    df = quitar_duplicados(df)
    return df.reset_index(drop=True), incoherentes


def guardar(df, ruta):
    """Crea la carpeta de salida si hace falta y guarda el CSV en UTF-8."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ruta, index=False, encoding="utf-8")


def limpiar_retos():
    """Punto de entrada: lee, diagnostica, limpia, diagnostica de nuevo y guarda."""
    # Opcional: se puede pasar otra ruta de CSV como argumento.
    ruta = encontrar_archivo(sys.argv[1] if len(sys.argv) > 1 else None)
    df = leer_datos(ruta)

    faltantes = [c for c in COLUMNAS_OBLIGATORIAS + ["descripcion"] if c not in df.columns]
    if faltantes:
        sys.exit(f"ERROR: faltan columnas en el CSV: {faltantes}")

    nulos_antes = df.isna().sum()
    filas_antes = len(df)
    imprimir_diagnostico(df, "ANTES de limpiar")

    df, incoherentes = limpiar(df)

    imprimir_diagnostico(df, "DESPUÉS de limpiar")

    print(f"\n{'=' * 60}\nRESUMEN\n{'=' * 60}")
    print("Nulos corregidos por columna (antes -> después):")
    for columna in nulos_antes.index:
        print(f"  {columna}: {nulos_antes[columna]} -> {df[columna].isna().sum()}")
    print(f"Fechas incoherentes (fin antes que inicio): {incoherentes}")
    print(f"Filas antes: {filas_antes} | filas después: {len(df)}")
    print(f"Filas eliminadas: {filas_antes - len(df)}")

    guardar(df, RUTA_SALIDA)
    print(f"\nArchivo limpio guardado en: {RUTA_SALIDA}")


if __name__ == "__main__":
    limpiar_retos()