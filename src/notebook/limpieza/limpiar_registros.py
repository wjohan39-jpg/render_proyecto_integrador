from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
COLUMNAS_REQUERIDAS = (
    "id",
    "fecha_registro",
    "observacion",
    "estado",
    "id_usuario",
    "id_reto",
)


def _diagnostico(df: pd.DataFrame, titulo: str) -> None:
    print(f"\n{titulo}")
    print(f"Shape: {df.shape}")
    df.info()
    print("Nulos por columna:")
    print(df.isna().sum())
    print(f"Duplicados exactos: {df.duplicated().sum()}")


def limpiar_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    faltantes = sorted(set(COLUMNAS_REQUERIDAS) - set(df.columns))
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {', '.join(faltantes)}")

    df = df.copy()
    filas_iniciales = len(df)
    _diagnostico(df, "Diagnostico inicial")

    df = df.drop_duplicates()
    df["fecha_registro"] = pd.to_datetime(
        df["fecha_registro"], format="mixed", dayfirst=True, errors="coerce"
    )
    df["estado"] = (
        df["estado"].astype("string").str.strip().str.upper().str.replace(" ", "_", regex=False)
    )
    df["observacion"] = df["observacion"].fillna("Sin observacion")

    repetidos = df[df.duplicated(subset=["id_usuario", "id_reto"], keep=False)]
    print(f"Participaciones repetidas (usuario y reto): {len(repetidos)}")
    df = df.drop_duplicates(subset=["id_usuario", "id_reto"], keep="first")
    df["mes"] = df["fecha_registro"].dt.to_period("M")

    if df[list(COLUMNAS_REQUERIDAS)].isna().any().any():
        raise ValueError("La limpieza produjo valores nulos en columnas requeridas.")

    print("\nDiagnostico final")
    print(f"Shape: {df.shape}")
    print("Nulos por columna:")
    print(df.isna().sum())
    print(f"Filas eliminadas: {filas_iniciales - len(df)}")
    return df


def limpiar_registros() -> pd.DataFrame:
    ruta_entrada = PROJECT_ROOT / "data" / "crudo" / "registros_sucio.csv"
    ruta_salida = PROJECT_ROOT / "data" / "limpio" / "registros_limpio.csv"
    if not ruta_entrada.exists():
        raise FileNotFoundError(f"No se encontro el archivo de entrada: {ruta_entrada}")

    df = limpiar_dataframe(pd.read_csv(ruta_entrada))
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ruta_salida, index=False, encoding="utf-8")
    print(f"Archivo limpio guardado en: {ruta_salida.relative_to(PROJECT_ROOT)}")
    return df


if __name__ == "__main__":
    limpiar_registros()