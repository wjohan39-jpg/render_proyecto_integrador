"""Base de datos del CRUD (empresas, prioridades, retos, registros y usuarios).

- Con la variable DATABASE_URL (por ejemplo la Internal Database URL de Render Postgres)
  se usa PostgreSQL y los datos se conservan entre despliegues.
- Sin DATABASE_URL (desarrollo local) se usa SQLite en data/integrador.db.

La primera vez que arranca la API se crean las tablas y se cargan los CSV limpios
de data/limpio/. A partir de ahi los cambios del CRUD viven en la base de datos;
los CSV y las graficas de main.py no se modifican.
"""
import os
import re
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
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
USA_POSTGRES = DATABASE_URL.startswith(("postgres://", "postgresql://"))

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


def traducir_a_postgres(sql: str) -> str:
    """Convierte el SQL escrito para SQLite al dialecto de PostgreSQL."""
    ignorar = sql.lstrip().upper().startswith("INSERT OR IGNORE")
    sql = re.sub(r"INSERT OR IGNORE INTO", "INSERT INTO", sql, flags=re.IGNORECASE)
    sql = re.sub(r"([\w.]+) COLLATE NOCASE", r"LOWER(\1)", sql)
    sql = sql.replace("?", "%s")
    return f"{sql} ON CONFLICT DO NOTHING" if ignorar else sql


class ConexionPostgres:
    """Envuelve psycopg con la misma interfaz de sqlite3 que usa el resto de la API."""

    def __init__(self, con):
        self._con = con

    def execute(self, sql: str, parametros=()):
        return self._con.execute(traducir_a_postgres(sql), tuple(parametros) or None)

    def executemany(self, sql: str, filas) -> None:
        with self._con.cursor() as cursor:
            cursor.executemany(traducir_a_postgres(sql), list(filas))

    def executescript(self, sql: str) -> None:
        self._con.execute(sql)

    def commit(self) -> None:
        self._con.commit()

    def rollback(self) -> None:
        self._con.rollback()

    def close(self) -> None:
        self._con.close()


def conectar():
    if USA_POSTGRES:
        import psycopg
        from psycopg.rows import dict_row

        return ConexionPostgres(psycopg.connect(DATABASE_URL, row_factory=dict_row))
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
    enteros = {"empresas": ["activa"], "prioridades": ["nivel", "dias_max_respuesta"]}.get(tabla, [])
    if tabla == "empresas":
        df["activa"] = (df["activa"].str.lower() == "true").astype(int).astype(str)
    # Tuplas con tipos de Python (int/str): psycopg no acepta los enteros de numpy.
    filas = [
        tuple(int(v) if c in enteros else v for c, v in zip(columnas, fila))
        for fila in df.itertuples(index=False, name=None)
    ]
    marcas = ", ".join("?" for _ in columnas)
    con.executemany(f"INSERT OR IGNORE INTO {tabla} ({', '.join(columnas)}) VALUES ({marcas})", filas)


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
    if DATABASE_URL and not USA_POSTGRES:
        raise RuntimeError("DATABASE_URL debe empezar por postgresql:// (revisa que no tenga comillas ni espacios).")
    if USA_POSTGRES:
        print("Base de datos: PostgreSQL (DATABASE_URL)", flush=True)
    else:
        motivo = "DATABASE_URL existe pero esta vacia" if "DATABASE_URL" in os.environ else "no hay DATABASE_URL"
        parecidas = [k for k in os.environ if "DATABASE" in k.upper() and k != "DATABASE_URL"]
        if parecidas:
            motivo += f"; variables con nombre parecido: {parecidas}"
        print(f"Base de datos: SQLite ({RUTA_DB}); {motivo}. Los datos no persisten en Render.", flush=True)
        RUTA_DB.parent.mkdir(parents=True, exist_ok=True)
    with conexion() as con:
        con.executescript(ESQUEMA)
        for tabla in COLUMNAS_CSV:
            if con.execute(f"SELECT COUNT(*) AS total FROM {tabla}").fetchone()["total"] == 0:
                _cargar_csv(con, tabla)
        if con.execute("SELECT COUNT(*) AS total FROM usuarios").fetchone()["total"] == 0:
            _crear_admin(con)
