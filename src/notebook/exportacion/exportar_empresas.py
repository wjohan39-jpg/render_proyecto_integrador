import os
from simulacion.simular_empresas import generar_empresas

CARPETA = os.path.join("data", "crudo")


def exportar_empresas(carpeta=CARPETA):
    os.makedirs(carpeta, exist_ok=True)
    df = generar_empresas()

    ruta_csv = os.path.join(carpeta, "empresas_sucio.csv")
    ruta_xlsx = os.path.join(carpeta, "empresas_sucio.xlsx")
    ruta_json = os.path.join(carpeta, "empresas_sucio.json")

    df.to_csv(ruta_csv, index=False, encoding="utf-8")
    df.to_excel(ruta_xlsx, index=False, sheet_name="empresas")
    df.to_json(ruta_json, orient="records", force_ascii=False, indent=2)

    for ruta in (ruta_csv, ruta_xlsx, ruta_json):
        print(f"{ruta} -> {df.shape}")

    return df


if __name__ == "__main__":
    exportar_empresas()