"""Base de datos del CRUD (empresas, prioridades, retos, registros y usuarios).

- Con la variable DATABASE_URL (por ejemplo la Internal Database URL de Render Postgres)
  se usa PostgreSQL y los datos se conservan entre despliegues.
- En el computador local se usa el MySQL de XAMPP (mysql://root@127.0.0.1:3306/integrador_relacional,
  se puede cambiar con MYSQL_URL), con claves foraneas reales visibles en phpMyAdmin.
- En Render sin DATABASE_URL (variable RENDER definida) se usa SQLite en data/integrador.db.

La primera vez que arranca la API se crean las tablas y se cargan los CSV limpios
de data/limpio/. A partir de ahi los cambios del CRUD viven en la base de datos;
los CSV y las graficas de main.py no se modifican.
"""
import os
import re
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import date, datetime
from pathlib import Path
from urllib.parse import unquote, urlparse

import pandas as pd

from api.seguridad import cifrar_contrasena

RAIZ = Path(__file__).resolve().parents[1]
CARPETA_LIMPIO = RAIZ / "data" / "limpio"
RUTA_DB = Path(os.getenv("DB_PATH", RAIZ / "data" / "integrador.db"))
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
USA_POSTGRES = DATABASE_URL.startswith(("postgres://", "postgresql://"))
# En el computador local la base de datos es siempre el MySQL de XAMPP. Render define la
# variable RENDER: alli se usa DATABASE_URL (Postgres) y SQLite solo como ultimo recurso.
MYSQL_URL = os.getenv("MYSQL_URL", "").strip() or (
    "" if os.getenv("RENDER") else "mysql://root@127.0.0.1:3306/integrador_relacional"
)
USA_MYSQL = not USA_POSTGRES and MYSQL_URL.startswith("mysql://")


class ErrorReferencia(Exception):
    """Un campo id_* apunta a un elemento que no existe (clave foranea de MySQL)."""

    def __init__(self, columna: str):
        super().__init__(columna)
        self.columna = columna

# Esquema para MySQL/MariaDB (XAMPP). Igual al de SQLite, pero con tipos de MySQL y las
# relaciones del diagrama (docs/diagrama_relacional.html) como FOREIGN KEY.
# Los CSV simulados traen ids que no existen en las otras tablas, por eso se cargan con
# FOREIGN_KEY_CHECKS = 0; lo nuevo que se cree desde la web si se valida.
ESQUEMA_MYSQL = """
CREATE TABLE IF NOT EXISTS usuarios (
    id CHAR(36) PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    correo VARCHAR(150) NOT NULL UNIQUE,
    rol VARCHAR(30) NOT NULL,
    activo TINYINT(1) NOT NULL DEFAULT 1,
    contrasena VARCHAR(255) NOT NULL,
    fecha_registro VARCHAR(19) NOT NULL
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS sesiones (
    token VARCHAR(100) PRIMARY KEY,
    id_usuario CHAR(36) NOT NULL,
    expira VARCHAR(19) NOT NULL,
    CONSTRAINT fk_sesiones_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS empresas (
    id CHAR(36) PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    nit VARCHAR(30) NOT NULL,
    sector VARCHAR(80) NOT NULL,
    contacto VARCHAR(150) NOT NULL,
    correo VARCHAR(150) NOT NULL,
    telefono VARCHAR(30) NOT NULL,
    activa TINYINT(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS prioridades (
    id CHAR(36) PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    nivel INT NOT NULL,
    dias_max_respuesta INT NOT NULL
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS categorias (
    id VARCHAR(36) PRIMARY KEY
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS retos (
    id CHAR(36) PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    estado VARCHAR(30) NOT NULL,
    id_empresa CHAR(36),
    id_categoria VARCHAR(36),
    id_prioridad CHAR(36),
    CONSTRAINT fk_retos_empresa FOREIGN KEY (id_empresa) REFERENCES empresas(id) ON DELETE SET NULL,
    CONSTRAINT fk_retos_categoria FOREIGN KEY (id_categoria) REFERENCES categorias(id) ON DELETE SET NULL,
    CONSTRAINT fk_retos_prioridad FOREIGN KEY (id_prioridad) REFERENCES prioridades(id) ON DELETE SET NULL
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS registros (
    id CHAR(36) PRIMARY KEY,
    fecha_registro DATETIME NOT NULL,
    observacion TEXT NOT NULL,
    estado VARCHAR(30) NOT NULL,
    id_usuario CHAR(36),
    id_reto CHAR(36),
    CONSTRAINT fk_registros_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE SET NULL,
    CONSTRAINT fk_registros_reto FOREIGN KEY (id_reto) REFERENCES retos(id) ON DELETE SET NULL
) ENGINE=InnoDB;
"""

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


def traducir_a_mysql(sql: str) -> str:
    """Convierte el SQL escrito para SQLite al dialecto de MySQL/MariaDB."""
    sql = re.sub(r"INSERT OR IGNORE INTO", "INSERT IGNORE INTO", sql, flags=re.IGNORECASE)
    sql = sql.replace(" COLLATE NOCASE", "")  # utf8mb4_unicode_ci ya ignora mayusculas
    return sql.replace("%", "%%").replace("?", "%s")


def _como_sqlite(fila: dict | None) -> dict | None:
    """Fechas de MySQL -> el mismo texto que guarda SQLite ('2026-07-17' / '2026-07-17 20:59:00')."""
    if fila is None:
        return None
    for clave, valor in fila.items():
        if isinstance(valor, datetime):
            fila[clave] = valor.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(valor, date):
            fila[clave] = valor.isoformat()
    return fila


class CursorMySQL:
    def __init__(self, cursor):
        self._cursor = cursor
        self.rowcount = cursor.rowcount

    def fetchone(self):
        return _como_sqlite(self._cursor.fetchone())

    def fetchall(self):
        return [_como_sqlite(f) for f in self._cursor.fetchall()]


class ConexionMySQL:
    """Envuelve PyMySQL con la misma interfaz de sqlite3 que usa el resto de la API."""

    def __init__(self, con):
        self._con = con

    def execute(self, sql: str, parametros=()):
        import pymysql

        cursor = self._con.cursor()
        try:
            cursor.execute(traducir_a_mysql(sql), tuple(parametros))
        except pymysql.err.IntegrityError as error:
            columna = re.search(r"FOREIGN KEY \(`(\w+)`\)", str(error))
            if error.args[0] == 1452 and columna:
                raise ErrorReferencia(columna.group(1)) from error
            raise
        return CursorMySQL(cursor)

    def executemany(self, sql: str, filas) -> None:
        with self._con.cursor() as cursor:
            cursor.executemany(traducir_a_mysql(sql), list(filas))

    def executescript(self, sql: str) -> None:
        with self._con.cursor() as cursor:
            for sentencia in filter(str.strip, sql.split(";")):
                cursor.execute(sentencia)

    def commit(self) -> None:
        self._con.commit()

    def rollback(self) -> None:
        self._con.rollback()

    def close(self) -> None:
        self._con.close()


def _conectar_mysql():
    import pymysql
    from pymysql.constants import CLIENT

    url = urlparse(MYSQL_URL)
    return ConexionMySQL(pymysql.connect(
        host=url.hostname or "127.0.0.1",
        port=url.port or 3306,
        user=unquote(url.username or "root"),
        password=unquote(url.password or ""),
        database=url.path.lstrip("/") or "integrador_relacional",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        # rowcount = filas encontradas (como SQLite), no solo las que cambiaron
        client_flag=CLIENT.FOUND_ROWS,
    ))


def _crear_base_mysql() -> None:
    """Crea la base de datos de MYSQL_URL si todavia no existe."""
    import pymysql

    url = urlparse(MYSQL_URL)
    nombre = url.path.lstrip("/") or "integrador_relacional"
    con = pymysql.connect(host=url.hostname or "127.0.0.1", port=url.port or 3306,
                          user=unquote(url.username or "root"), password=unquote(url.password or ""))
    try:
        with con.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{nombre}` "
                           "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    finally:
        con.close()


def conectar():
    if USA_MYSQL:
        return _conectar_mysql()
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
    elif USA_MYSQL:
        url = urlparse(MYSQL_URL)
        print(f"Base de datos: MySQL ({url.hostname}:{url.port or 3306}/{url.path.lstrip('/')}) (MYSQL_URL)", flush=True)
        try:
            _crear_base_mysql()
        except Exception as error:
            raise RuntimeError(
                f"No se pudo conectar al MySQL de XAMPP ({url.hostname}:{url.port or 3306}). "
                "Enciende MySQL en el panel de XAMPP y vuelve a iniciar la API."
            ) from error
    else:
        motivo = "DATABASE_URL existe pero esta vacia" if "DATABASE_URL" in os.environ else "no hay DATABASE_URL"
        parecidas = [k for k in os.environ if "DATABASE" in k.upper() and k != "DATABASE_URL"]
        if parecidas:
            motivo += f"; variables con nombre parecido: {parecidas}"
        print(f"Base de datos: SQLite ({RUTA_DB}); {motivo}. Los datos no persisten en Render.", flush=True)
        RUTA_DB.parent.mkdir(parents=True, exist_ok=True)
    with conexion() as con:
        con.executescript(ESQUEMA_MYSQL if USA_MYSQL else ESQUEMA)
        if USA_MYSQL:
            # Los ids de los CSV simulados no coinciden entre tablas: se cargan sin validar.
            con.execute("SET FOREIGN_KEY_CHECKS = 0")
        for tabla in COLUMNAS_CSV:
            if con.execute(f"SELECT COUNT(*) AS total FROM {tabla}").fetchone()["total"] == 0:
                _cargar_csv(con, tabla)
                if USA_MYSQL and tabla == "retos":
                    con.execute("INSERT IGNORE INTO categorias (id) SELECT DISTINCT id_categoria FROM retos "
                                "WHERE id_categoria IS NOT NULL AND id_categoria <> ''")
        if USA_MYSQL:
            con.execute("SET FOREIGN_KEY_CHECKS = 1")
        if con.execute("SELECT COUNT(*) AS total FROM usuarios").fetchone()["total"] == 0:
            _crear_admin(con)
