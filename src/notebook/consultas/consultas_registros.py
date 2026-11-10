from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]


def _guardar(resultado: pd.DataFrame | pd.Series, numero: int, titulo: str):
    if isinstance(resultado, pd.Series):
        resultado = resultado.to_frame()
    destino = PROJECT_ROOT / "data" / "limpio" / f"registros_consulta_{numero}.csv"
    resultado.to_csv(destino, index=True, encoding="utf-8")
    print(f"\nConsulta {numero} — {titulo}")
    print(resultado)
    return resultado


def consulta_1_finalizados(df: pd.DataFrame):
    finalizados = df[df["estado"] == "FINALIZADO"]
    return _guardar(finalizados, 1, "participaciones finalizadas")


def consulta_2_repetidos(df: pd.DataFrame):
    repetidos = df[df.duplicated(subset=["id_usuario", "id_reto"], keep=False)]
    return _guardar(repetidos, 2, "participaciones repetidas por usuario y reto")


def consulta_3_por_estado(df: pd.DataFrame):
    conteo = df["estado"].value_counts()
    return _guardar(conteo, 3, "participaciones por estado")


def consulta_4_top_retos(df: pd.DataFrame):
    top_retos = df.groupby("id_reto")["id"].count().nlargest(10)
    return _guardar(top_retos, 4, "10 retos con mas participantes")


def consulta_5_por_mes(df: pd.DataFrame):
    por_mes = df.groupby("mes")["id"].count()
    return _guardar(por_mes, 5, "participaciones por mes")


def ejecutar_consultas() -> list[pd.DataFrame]:
    ruta = PROJECT_ROOT / "data" / "limpio" / "registros_limpio.csv"
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontro el archivo limpio: {ruta}")

    df = pd.read_csv(ruta, parse_dates=["fecha_registro"])
    df["mes"] = pd.PeriodIndex(df["mes"], freq="M")
    consultas = (
        consulta_1_finalizados,
        consulta_2_repetidos,
        consulta_3_por_estado,
        consulta_4_top_retos,
        consulta_5_por_mes,
    )
    return [consulta(df) for consulta in consultas]


if __name__ == "__main__":
    ejecutar_consultas()