import os
from importlib import import_module

simulacion = import_module("src.notebook.simulacion.simular_prioridades")
generar_prioridades = simulacion.generar_prioridades

RUTA_CARPETA = "data/crudo"


def exportar():
    os.makedirs(RUTA_CARPETA, exist_ok=True)
    df = generar_prioridades()

    ruta_csv = os.path.join(RUTA_CARPETA, "prioridades_sucio.csv")
    ruta_xlsx = os.path.join(RUTA_CARPETA, "prioridades_sucio.xlsx")
    ruta_json = os.path.join(RUTA_CARPETA, "prioridades_sucio.json")

    df.to_csv(ruta_csv, index=False, encoding="utf-8")
    df.to_excel(ruta_xlsx, index=False, sheet_name="prioridades")
    df.to_json(ruta_json, orient="records", force_ascii=False, indent=2)

    for ruta in (ruta_csv, ruta_xlsx, ruta_json):
        print(f"{ruta} -> {df.shape}")


if __name__ == "__main__":
    exportar()