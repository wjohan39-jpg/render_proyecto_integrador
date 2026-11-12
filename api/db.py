"""Base de datos SQLite para el CRUD (empresas, prioridades, retos, registros y usuarios).

La primera vez que arranca la API se crean las tablas y se cargan los CSV limpios
de data/limpio/. A partir de ahi los cambios del CRUD viven en la base de datos;
los CSV y las graficas de main.py no se modifican.
"""
import os
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

import pandas as pd

from api.seguridad import cifrar_contrasena

RAIZ = Path(__file__).resolve().parents[1]
CARPETA_LIMPIO = RAIZ / "data" / "limpio"
RUTA_DB = Path(os.getenv("DB_PATH", RAIZ / "data" / "integrador.db"))

ESQUEMA = """
CREATE TABLE IF NOT EXISTS usuarios (
    id TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL UNIQUE,
    rol TEXT NOT NULL,
    activo INTEGER NOT NULL DEFAULT 1,
    contrasena TEXT NOT NULL,
    fecha_registro TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS sesiones (
    token TEXT PRIMARY KEY,
    id_usuario TEXT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    expira TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS empresas (
    id TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    nit TEXT NOT NULL,
    sector TEXT NOT NULL,
    contacto TEXT NOT NULL,
    correo TEXT NOT NULL,
    telefono TEXT NOT NULL,
    activa INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS prioridades (
    id TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    nivel INTEGER NOT NULL,
    dias_max_respuesta INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS retos (
    id TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_inicio TEXT NOT NULL,
    fecha_fin TEXT NOT NULL,
    estado TEXT NOT NULL,
    id_empresa TEXT,
    id_categoria TEXT,
    id_prioridad TEXT
);
CREATE TABLE IF NOT EXISTS registros (
    id TEXT PRIMARY KEY,
    fecha_registro TEXT NOT NULL,
    observacion TEXT NOT NULL,
    estado TEXT NOT NULL,
    id_usuario TEXT,
    id_reto TEXT
);
"""

# Columnas que se toman de cada CSV limpio (las calculadas, como duracion_dias, se omiten).
COLUMNAS_CSV = {
    "empresas": ["id", "nombre", "nit", "sector", "contacto", "correo", "telefono", "activa"],
    "prioridades": ["id", "nombre", "nivel", "dias_max_respuesta"],
    "retos": ["id", "nombre", "descripcion", "fecha_inicio", "fecha_fin", "estado",
              "id_empresa", "id_categoria", "id_prioridad"],
    "registros": ["id", "fecha_registro", "observacion", "estado", "id_usuario", "id_reto"],
}


def nuevo_id() -> str:
    return str(uuid.uuid4())


def ahora() -> str:
    return datetime.now().isoformat(timespec="seconds")


def conectar() -> sqlite3.Connection:
    con = sqlite3.connect(RUTA_DB)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


@contextmanager
def conexion():
    """Abre una conexion, confirma los cambios si todo sale bien y la cierra."""
    con = conectar()
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def _cargar_csv(con: sqlite3.Connection, tabla: str) -> None:
    ruta = CARPETA_LIMPIO / f"{tabla}_limpio.csv"
    if not ruta.exists():
        return
    columnas = COLUMNAS_CSV[tabla]
    df = pd.read_csv(ruta, dtype=str, keep_default_na=False)[columnas]
    df = df.apply(lambda s: s.str.strip())
    if tabla == "empresas":
        df["activa"] = (df["activa"].str.lower() == "true").astype(int)
    marcas = ", ".join("?" for _ in columnas)
    con.executemany(
        f"INSERT OR IGNORE INTO {tabla} ({', '.join(columnas)}) VALUES ({marcas})",
        df.itertuples(index=False, name=None),
    )


def _crear_admin(con: sqlite3.Connection) -> None:
    """Usuario administrador inicial (la contrasena se puede cambiar con ADMIN_PASSWORD)."""
    correo = os.getenv("ADMIN_EMAIL", "admin@cesde.edu.co").lower()
    contrasena = os.getenv("ADMIN_PASSWORD", "Admin123*")
    con.execute(
        "INSERT INTO usuarios (id, nombre, correo, rol, activo, contrasena, fecha_registro) "
        "VALUES (?, ?, ?, 'administrador', 1, ?, ?)",
        (nuevo_id(), "Administrador", correo, cifrar_contrasena(contrasena), ahora()),
    )


def inicializar() -> None:
    """Crea las tablas y, si estan vacias, las llena con los CSV limpios."""
    RUTA_DB.parent.mkdir(parents=True, exist_ok=True)
    with conexion() as con:
        con.executescript(ESQUEMA)
        for tabla in COLUMNAS_CSV:
            if con.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0] == 0:
                _cargar_csv(con, tabla)
        if con.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0] == 0:
            _crear_admin(con)
