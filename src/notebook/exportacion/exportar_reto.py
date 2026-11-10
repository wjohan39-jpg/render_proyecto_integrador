"""Exporta la tabla retos sucia a CSV, XLSX y JSON (HU X01 de Kaizen).

Uso:
    python src/notebook/exportacion/exportar_reto.py

Genera los datos con simular_reto.py y los guarda en data/crudo/.
"""

import sys
from pathlib import Path

# Carpeta src/notebook/ (este archivo está en src/notebook/exportacion/)
CARPETA_NOTEBOOK = Path(__file__).resolve().parents[1]

# Permite importar simular_reto.py desde la carpeta simulacion
sys.path.insert(0, str(CARPETA_NOTEBOOK / "simulacion"))
from simular_reto import generar_retos

# Raíz del proyecto: integrador_diego_zea/
RAIZ = Path(__file__).resolve().parents[3]
CARPETA_CRUDO = RAIZ / "data" / "crudo"


def exportar_retos(n=500):
    """Genera n retos sucios y los guarda en CSV, XLSX y JSON. Devuelve el DataFrame."""
    # La carpeta se crea sola si no existe
    CARPETA_CRUDO.mkdir(parents=True, exist_ok=True)

    df = generar_retos(n)

    ruta_csv = CARPETA_CRUDO / "retos_sucio.csv"
    ruta_xlsx = CARPETA_CRUDO / "retos_sucio.xlsx"
    ruta_json = CARPETA_CRUDO / "retos_sucio.json"

    df.to_csv(ruta_csv, index=False, encoding="utf-8")
    df.to_excel(ruta_xlsx, index=False, sheet_name="retos")
    df.to_json(ruta_json, orient="records", force_ascii=False, indent=2)

    for ruta in (ruta_csv, ruta_xlsx, ruta_json):
        print(f"{ruta} -> {df.shape}")

    return df


if __name__ == "__main__":
    exportar_retos()