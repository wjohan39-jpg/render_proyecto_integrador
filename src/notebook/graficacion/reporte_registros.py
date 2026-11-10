from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]


def generar_reporte() -> list[Path]:
    ruta_limpia = PROJECT_ROOT / "data" / "limpio" / "registros_limpio.csv"
    ruta_cruda = PROJECT_ROOT / "data" / "crudo" / "registros_sucio.csv"
    if not ruta_limpia.exists():
        raise FileNotFoundError(f"No se encontro el archivo limpio: {ruta_limpia}")

    df = pd.read_csv(ruta_limpia, parse_dates=["fecha_registro"])
    df["mes"] = pd.PeriodIndex(df["mes"], freq="M")
    reportes = PROJECT_ROOT / "reportes"
    reportes.mkdir(parents=True, exist_ok=True)

    conteo = df["estado"].value_counts()
    por_mes = df.groupby("mes")["id"].count()
    top_retos = df.groupby("id_reto")["id"].count().nlargest(10).sort_values()
    rutas = [reportes / f"registros_grafica_{numero}.png" for numero in range(1, 4)]

    conteo.plot(kind="bar")
    plt.title("Participaciones por estado")
    plt.xlabel("Estado")
    plt.ylabel("Cantidad de participaciones")
    plt.tight_layout()
    plt.savefig(rutas[0], dpi=120)
    plt.close()

    por_mes.plot(kind="line", marker="o")
    plt.title("Participaciones por mes")
    plt.xlabel("Mes")
    plt.ylabel("Cantidad de participaciones")
    plt.tight_layout()
    plt.savefig(rutas[1], dpi=120)
    plt.close()

    top_retos.plot(kind="barh")
    plt.title("10 retos con mas participantes")
    plt.xlabel("Cantidad de participantes")
    plt.ylabel("Reto")
    plt.tight_layout()
    plt.savefig(rutas[2], dpi=120)
    plt.close()

    reto_popular = df.groupby("id_reto")["id"].count().idxmax()
    cantidad_popular = int(df.groupby("id_reto")["id"].count().max())
    mes_pico = por_mes.idxmax()
    cantidad_mes_pico = int(por_mes.max())
    duplicados = 0
    if ruta_cruda.exists():
        datos_crudos = pd.read_csv(ruta_cruda)
        duplicados = int(
            datos_crudos.duplicated(subset=["id_usuario", "id_reto"], keep=False).sum()
        )

    print("\nConclusiones")
    print(f"Reto mas popular: {reto_popular} ({cantidad_popular} participantes).")
    print(f"Mes con mas inscripciones: {mes_pico} ({cantidad_mes_pico} inscripciones).")
    print(f"Inscripciones repetidas detectadas en los datos sucios: {duplicados}.")
    print("El backend debe responder 409 Conflict ante una inscripcion repetida del mismo usuario al mismo reto.")
    for ruta in rutas:
        print(f"Grafica: {ruta.relative_to(PROJECT_ROOT)}")
    return rutas


if __name__ == "__main__":
    generar_reporte()