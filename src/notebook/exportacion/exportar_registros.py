from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.notebook.simulacion.simular_registros import generar_registros


def exportar_registros():
    carpeta = PROJECT_ROOT / "data" / "crudo"
    carpeta.mkdir(parents=True, exist_ok=True)
    df = generar_registros()

    rutas = {
        "CSV": carpeta / "registros_sucio.csv",
        "XLSX": carpeta / "registros_sucio.xlsx",
        "JSON": carpeta / "registros_sucio.json",
    }
    df.to_csv(rutas["CSV"], index=False, encoding="utf-8")
    df.to_excel(rutas["XLSX"], index=False, sheet_name="registros")
    df.to_json(rutas["JSON"], orient="records", force_ascii=False, indent=2)

    for formato, ruta in rutas.items():
        print(f"{formato}: {ruta.relative_to(PROJECT_ROOT)} | shape={df.shape}")
    return df


if __name__ == "__main__":
    exportar_registros()