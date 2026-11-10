"""API REST de solo lectura sobre los resultados de main.py.

Ejecutar en local (desde la raiz del proyecto):
    uvicorn api.app:app --reload

Documentacion interactiva: http://127.0.0.1:8000/docs
"""
import math
import os
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from api.catalogo import MODULOS

RAIZ = Path(__file__).resolve().parents[1]
CARPETA_LIMPIO = RAIZ / "data" / "limpio"
CARPETA_REPORTES = RAIZ / "reportes"

app = FastAPI(
    title="API Proyecto integrador",
    description="Prioridades (Dave), registros (Jeferson), empresas (Wesly) y retos (Diego).",
    version="1.0.0",
)

# Origenes permitidos separados por coma; por defecto cualquiera (la API es de solo lectura).
origenes = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origenes, allow_methods=["GET"], allow_headers=["*"])


# ----------------------------- utilidades -----------------------------
def _modulo(modulo_id: str) -> dict:
    if modulo_id not in MODULOS:
        raise HTTPException(status_code=404, detail=f"No existe la sección '{modulo_id}'.")
    return MODULOS[modulo_id]


def _leer_csv(ruta: Path) -> pd.DataFrame:
    if not ruta.exists():
        raise HTTPException(status_code=404, detail=f"No se encontró {ruta.name}. Ejecuta main.py.")
    df = pd.read_csv(ruta)
    # Algunas consultas se guardaron con el indice sin nombre.
    return df.rename(columns=lambda c: "indice" if str(c).startswith("Unnamed") else c)


def _a_json(df: pd.DataFrame) -> list[dict]:
    """Convierte el DataFrame en filas JSON (NaN -> null)."""
    filas = df.astype(object).to_dict(orient="records")
    return [
        {k: (None if isinstance(v, float) and math.isnan(v) else v) for k, v in fila.items()}
        for fila in filas
    ]


def _validar_numero(numero: int, total: int, que: str) -> None:
    if not 1 <= numero <= total:
        raise HTTPException(status_code=404, detail=f"La {que} {numero} no existe (1 a {total}).")


# ----------------------------- endpoints -----------------------------
@app.get("/api/salud", tags=["general"])
def salud():
    return {"estado": "ok"}


@app.get("/api/modulos", tags=["general"])
def listar_modulos():
    """Secciones disponibles, en el orden del panel."""
    return [{"id": mid, "nombre": m["nombre"], "autor": m["autor"]} for mid, m in MODULOS.items()]


@app.get("/api/modulos/{modulo_id}", tags=["modulos"])
def detalle_modulo(modulo_id: str):
    """Textos de la sección, sus gráficas, sus consultas y el total de filas limpias."""
    m = _modulo(modulo_id)
    ruta_limpio = CARPETA_LIMPIO / f"{m['prefijo']}_limpio.csv"
    total = len(pd.read_csv(ruta_limpio)) if ruta_limpio.exists() else 0
    return {
        "id": modulo_id,
        "nombre": m["nombre"],
        "autor": m["autor"],
        "sobretitulo": m["sobretitulo"],
        "titulo": m["nombre"],
        "resumen": m["resumen"],
        "pie": m["pie"],
        "totalRegistros": total,
        "graficas": [
            {
                "numero": n,
                "titulo": titulo,
                "descripcion": descripcion,
                "alt": alt,
                "url": f"/api/modulos/{modulo_id}/graficas/{n}",
            }
            for n, (titulo, descripcion, alt) in enumerate(m["graficas"], start=1)
        ],
        "consultas": [
            {"numero": n, "titulo": titulo, "url": f"/api/modulos/{modulo_id}/consultas/{n}"}
            for n, titulo in enumerate(m["consultas"], start=1)
        ],
    }


@app.get("/api/modulos/{modulo_id}/consultas/{numero}", tags=["modulos"])
def consulta(modulo_id: str, numero: int):
    """Resultado de una de las cinco consultas (data/limpio/<prefijo>_consulta_N.csv)."""
    m = _modulo(modulo_id)
    _validar_numero(numero, len(m["consultas"]), "consulta")
    df = _leer_csv(CARPETA_LIMPIO / f"{m['prefijo']}_consulta_{numero}.csv")
    return {
        "numero": numero,
        "titulo": m["consultas"][numero - 1],
        "columnas": list(df.columns),
        "total": len(df),
        "filas": _a_json(df),
    }


@app.get("/api/modulos/{modulo_id}/datos", tags=["modulos"])
def datos(
    modulo_id: str,
    pagina: int = Query(1, ge=1),
    tamano: int = Query(20, ge=1, le=200),
):
    """Datos limpios paginados (data/limpio/<prefijo>_limpio.csv)."""
    m = _modulo(modulo_id)
    df = _leer_csv(CARPETA_LIMPIO / f"{m['prefijo']}_limpio.csv")
    inicio = (pagina - 1) * tamano
    return {
        "pagina": pagina,
        "tamano": tamano,
        "total": len(df),
        "columnas": list(df.columns),
        "filas": _a_json(df.iloc[inicio:inicio + tamano]),
    }


@app.get("/api/modulos/{modulo_id}/graficas/{numero}", tags=["modulos"], response_class=FileResponse)
def grafica(modulo_id: str, numero: int):
    """Imagen PNG de la gráfica (reportes/<prefijo>_grafica_N.png)."""
    m = _modulo(modulo_id)
    _validar_numero(numero, len(m["graficas"]), "gráfica")
    ruta = CARPETA_REPORTES / f"{m['prefijo']}_grafica_{numero}.png"
    if not ruta.exists():
        raise HTTPException(status_code=404, detail=f"No se encontró {ruta.name}. Ejecuta main.py.")
    return FileResponse(ruta, media_type="image/png")
