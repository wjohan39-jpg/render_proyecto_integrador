"""Endpoints CRUD: listar, consultar, crear, modificar y eliminar.

    GET    /api/{recurso}        lista completa
    GET    /api/{recurso}/{id}   un elemento
    POST   /api/{recurso}        crear
    PUT    /api/{recurso}/{id}   modificar
    DELETE /api/{recurso}/{id}   eliminar

Todos exigen sesion iniciada; /api/usuarios ademas exige rol administrador.
"""
from typing import Callable

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel

from api import db
from api.auth import solo_administrador, usuario_actual, usuario_publico
from api.esquemas import Empresa, Prioridad, RegistroParticipacion, Reto, Usuario
from api.seguridad import cifrar_contrasena


def _no_existe(recurso: str) -> HTTPException:
    return HTTPException(status.HTTP_404_NOT_FOUND, f"No se encontró el elemento en {recurso}.")


_NOMBRES_RELACION = {"id_empresa": "La empresa", "id_categoria": "La categoría", "id_prioridad": "La prioridad",
                     "id_usuario": "El usuario", "id_reto": "El reto"}


def _referencia_invalida(error: db.ErrorReferencia) -> HTTPException:
    """Con MySQL las claves foraneas exigen que el id elegido exista en su tabla."""
    texto = f"{_NOMBRES_RELACION.get(error.columna, error.columna)} indicada no existe."
    return HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, {"message": texto, "fields": {error.columna: texto}})


def crear_router(
    recurso: str,
    modelo: type[BaseModel],
    orden: str,
    convertir: Callable[[dict], dict] = lambda fila: fila,
    preparar: Callable[[dict], dict] = lambda datos: datos,
) -> APIRouter:
    """Router CRUD generico para una tabla cuyo nombre coincide con el recurso."""
    router = APIRouter(prefix=f"/api/{recurso}", tags=[recurso], dependencies=[Depends(usuario_actual)])

    def leer(con, id_: str) -> dict:
        fila = con.execute(f"SELECT * FROM {recurso} WHERE id = ?", (id_,)).fetchone()
        if fila is None:
            raise _no_existe(recurso)
        return convertir(dict(fila))

    @router.get("")
    def listar():
        with db.conexion() as con:
            filas = con.execute(f"SELECT * FROM {recurso} ORDER BY {orden}").fetchall()
        return [convertir(dict(f)) for f in filas]

    @router.get("/{id_}")
    def obtener(id_: str):
        with db.conexion() as con:
            return leer(con, id_)

    @router.post("", status_code=status.HTTP_201_CREATED)
    def crear(datos: modelo):  # type: ignore[valid-type]
        valores = {"id": db.nuevo_id(), **preparar(datos.model_dump(mode="json"))}
        columnas = ", ".join(valores)
        marcas = ", ".join("?" for _ in valores)
        try:
            with db.conexion() as con:
                con.execute(f"INSERT INTO {recurso} ({columnas}) VALUES ({marcas})", tuple(valores.values()))
                return leer(con, valores["id"])
        except db.ErrorReferencia as error:
            raise _referencia_invalida(error) from error

    @router.put("/{id_}")
    def modificar(id_: str, datos: modelo):  # type: ignore[valid-type]
        valores = preparar(datos.model_dump(mode="json"))
        asignaciones = ", ".join(f"{c} = ?" for c in valores)
        try:
            with db.conexion() as con:
                cursor = con.execute(f"UPDATE {recurso} SET {asignaciones} WHERE id = ?", (*valores.values(), id_))
                if cursor.rowcount == 0:
                    raise _no_existe(recurso)
                return leer(con, id_)
        except db.ErrorReferencia as error:
            raise _referencia_invalida(error) from error

    @router.delete("/{id_}", status_code=status.HTTP_204_NO_CONTENT)
    def eliminar(id_: str):
        with db.conexion() as con:
            if con.execute(f"DELETE FROM {recurso} WHERE id = ?", (id_,)).rowcount == 0:
                raise _no_existe(recurso)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return router


def _empresa(fila: dict) -> dict:
    return {**fila, "activa": bool(fila["activa"])}


def _registro(datos: dict) -> dict:
    # "2026-07-17T20:59:00" -> "2026-07-17 20:59:00", el mismo formato del CSV
    return {**datos, "fecha_registro": datos["fecha_registro"].replace("T", " ")[:19]}


empresas = crear_router("empresas", Empresa, "nombre COLLATE NOCASE", convertir=_empresa)
prioridades = crear_router("prioridades", Prioridad, "nivel DESC, nombre")
retos = crear_router("retos", Reto, "fecha_inicio DESC")
registros = crear_router("registros", RegistroParticipacion, "fecha_registro DESC", preparar=_registro)


# ----------------------------- usuarios -----------------------------
usuarios = APIRouter(prefix="/api/usuarios", tags=["usuarios"])


def _correo_libre(con, correo: str, excepto: str | None = None) -> None:
    fila = con.execute("SELECT id FROM usuarios WHERE correo = ?", (correo,)).fetchone()
    if fila and fila["id"] != excepto:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            {"message": "Ya existe un usuario con ese correo.", "fields": {"correo": "Este correo ya está registrado."}},
        )


def _leer_usuario(con, id_: str) -> dict:
    fila = con.execute("SELECT * FROM usuarios WHERE id = ?", (id_,)).fetchone()
    if fila is None:
        raise _no_existe("usuarios")
    return usuario_publico(fila)


@usuarios.get("")
def listar_usuarios(_: dict = Depends(solo_administrador)):
    with db.conexion() as con:
        filas = con.execute("SELECT * FROM usuarios ORDER BY nombre COLLATE NOCASE").fetchall()
    return [usuario_publico(f) for f in filas]


@usuarios.get("/{id_}")
def obtener_usuario(id_: str, _: dict = Depends(solo_administrador)):
    with db.conexion() as con:
        return _leer_usuario(con, id_)


@usuarios.post("", status_code=status.HTTP_201_CREATED)
def crear_usuario(datos: Usuario, _: dict = Depends(solo_administrador)):
    if not datos.contrasena:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {"message": "La contraseña es obligatoria.", "fields": {"contrasena": "Escribe una contraseña."}},
        )
    id_ = db.nuevo_id()
    with db.conexion() as con:
        _correo_libre(con, datos.correo)
        con.execute(
            "INSERT INTO usuarios (id, nombre, correo, rol, activo, contrasena, fecha_registro) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (id_, datos.nombre, datos.correo, datos.rol, int(datos.activo), cifrar_contrasena(datos.contrasena), db.ahora()),
        )
        return _leer_usuario(con, id_)


@usuarios.put("/{id_}")
def modificar_usuario(id_: str, datos: Usuario, sesion: dict = Depends(solo_administrador)):
    if id_ == sesion["id"] and (datos.rol != "administrador" or not datos.activo):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No puedes quitarte el rol de administrador ni desactivarte.")
    with db.conexion() as con:
        _leer_usuario(con, id_)
        _correo_libre(con, datos.correo, excepto=id_)
        con.execute(
            "UPDATE usuarios SET nombre = ?, correo = ?, rol = ?, activo = ? WHERE id = ?",
            (datos.nombre, datos.correo, datos.rol, int(datos.activo), id_),
        )
        if datos.contrasena:
            con.execute("UPDATE usuarios SET contrasena = ? WHERE id = ?", (cifrar_contrasena(datos.contrasena), id_))
        if not datos.activo:
            con.execute("DELETE FROM sesiones WHERE id_usuario = ?", (id_,))
        return _leer_usuario(con, id_)


@usuarios.delete("/{id_}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(id_: str, sesion: dict = Depends(solo_administrador)):
    if id_ == sesion["id"]:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No puedes eliminar tu propia cuenta.")
    with db.conexion() as con:
        if con.execute("DELETE FROM usuarios WHERE id = ?", (id_,)).rowcount == 0:
            raise _no_existe("usuarios")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
