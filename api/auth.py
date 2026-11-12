"""Inicio de sesion, registro, sesion actual y cierre de sesion.

El token es opaco (no JWT): se guarda en la tabla sesiones y vence a las HORAS_SESION.
El cliente lo envia en la cabecera  Authorization: Bearer <token>.
"""
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Header, HTTPException, status

from api import db
from api.esquemas import Login, Registro
from api.seguridad import cifrar_contrasena, nuevo_token, verificar_contrasena

HORAS_SESION = 8

router = APIRouter(prefix="/api/auth", tags=["autenticación"])


def usuario_publico(fila) -> dict:
    """Datos del usuario que se pueden enviar al navegador (sin la contrasena)."""
    return {
        "id": fila["id"],
        "nombre": fila["nombre"],
        "correo": fila["correo"],
        "rol": fila["rol"],
        "activo": bool(fila["activo"]),
        "fecha_registro": fila["fecha_registro"],
    }


def _token_de(authorization: str | None) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Inicia sesión para continuar.")
    return authorization[7:].strip()


def usuario_actual(authorization: str | None = Header(default=None)) -> dict:
    """Dependencia: devuelve el usuario de la sesion o responde 401."""
    token = _token_de(authorization)
    with db.conexion() as con:
        fila = con.execute(
            "SELECT u.*, s.expira FROM sesiones s JOIN usuarios u ON u.id = s.id_usuario WHERE s.token = ?",
            (token,),
        ).fetchone()
        valida = fila is not None and fila["expira"] >= db.ahora() and fila["activo"]
        if not valida:
            con.execute("DELETE FROM sesiones WHERE token = ?", (token,))
    if not valida:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "La sesión expiró. Inicia sesión de nuevo.")
    return usuario_publico(fila)


def solo_administrador(usuario: dict = Depends(usuario_actual)) -> dict:
    if usuario["rol"] != "administrador":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo un administrador puede gestionar usuarios.")
    return usuario


def _abrir_sesion(con, id_usuario: str) -> str:
    token = nuevo_token()
    expira = (datetime.now() + timedelta(hours=HORAS_SESION)).isoformat(timespec="seconds")
    con.execute("DELETE FROM sesiones WHERE expira < ?", (db.ahora(),))
    con.execute("INSERT INTO sesiones (token, id_usuario, expira) VALUES (?, ?, ?)", (token, id_usuario, expira))
    return token


@router.post("/login")
def login(datos: Login):
    with db.conexion() as con:
        fila = con.execute("SELECT * FROM usuarios WHERE correo = ?", (datos.correo,)).fetchone()
        if fila is None or not verificar_contrasena(datos.contrasena, fila["contrasena"]):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Correo o contraseña incorrectos.")
        if not fila["activo"]:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Tu usuario está inactivo. Contacta al administrador.")
        token = _abrir_sesion(con, fila["id"])
    return {"token": token, "usuario": usuario_publico(fila)}


@router.post("/register", status_code=status.HTTP_201_CREATED)
def registrar(datos: Registro):
    with db.conexion() as con:
        if con.execute("SELECT 1 FROM usuarios WHERE correo = ?", (datos.correo,)).fetchone():
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                {"message": "Ya existe una cuenta con ese correo.", "fields": {"correo": "Este correo ya está registrado."}},
            )
        id_usuario = db.nuevo_id()
        con.execute(
            "INSERT INTO usuarios (id, nombre, correo, rol, activo, contrasena, fecha_registro) VALUES (?, ?, ?, ?, 1, ?, ?)",
            (id_usuario, datos.nombre, datos.correo, datos.rol, cifrar_contrasena(datos.contrasena), db.ahora()),
        )
        token = _abrir_sesion(con, id_usuario)
        fila = con.execute("SELECT * FROM usuarios WHERE id = ?", (id_usuario,)).fetchone()
    return {"token": token, "usuario": usuario_publico(fila)}


@router.get("/me")
def yo(usuario: dict = Depends(usuario_actual)):
    return usuario


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(authorization: str | None = Header(default=None)):
    token = _token_de(authorization)
    with db.conexion() as con:
        con.execute("DELETE FROM sesiones WHERE token = ?", (token,))
