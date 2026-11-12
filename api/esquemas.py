"""Modelos de entrada (validacion) del CRUD y de la autenticacion."""
import re
from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

SECTORES = ("Tecnologia", "Salud", "Manufactura", "Energia")
ESTADOS_RETO = ("PENDIENTE", "EN_PROGRESO", "EN_CURSO", "COMPLETADA", "CERRADO")
ESTADOS_REGISTRO = ("INSCRITO", "EN_PROCESO", "FINALIZADO")
ROLES = ("administrador", "empresario", "profesor")
ROLES_REGISTRO = ("empresario", "profesor")  # el registro publico no crea administradores
NIVELES_PRIORIDAD = {"Baja": 1, "Media": 2, "Alta": 3}

PATRON_CORREO = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
PATRON_CONTRASENA = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d]).{8,}$")
MENSAJE_CONTRASENA = "Mínimo 8 caracteres, con mayúscula, minúscula, número y símbolo."


def _texto(valor: str) -> str:
    return " ".join(str(valor).split())


def _correo(valor: str) -> str:
    valor = str(valor).strip().lower()
    if not PATRON_CORREO.match(valor):
        raise ValueError("El correo no es válido.")
    return valor


def _contrasena(valor: Optional[str]) -> Optional[str]:
    if valor is not None and not PATRON_CONTRASENA.match(valor):
        raise ValueError(MENSAJE_CONTRASENA)
    return valor


# ----------------------------- autenticacion -----------------------------
class Login(BaseModel):
    correo: str
    contrasena: str = Field(min_length=1)

    _c = field_validator("correo")(_correo)


class Registro(BaseModel):
    nombre: str = Field(min_length=3, max_length=120)
    correo: str
    contrasena: str
    rol: Literal[ROLES_REGISTRO]

    _n = field_validator("nombre")(_texto)
    _c = field_validator("correo")(_correo)
    _p = field_validator("contrasena")(_contrasena)


# ----------------------------- CRUD -----------------------------
class Empresa(BaseModel):
    nombre: str = Field(min_length=3, max_length=150)
    nit: str
    sector: Literal[SECTORES]
    contacto: str = Field(min_length=3, max_length=150)
    correo: str
    telefono: str
    activa: bool = True

    _t = field_validator("nombre", "contacto")(_texto)
    _c = field_validator("correo")(_correo)

    @field_validator("nit")
    @classmethod
    def _nit(cls, valor: str) -> str:
        digitos = re.sub(r"\D", "", valor)
        if not 8 <= len(digitos) <= 10:
            raise ValueError("El NIT debe tener entre 8 y 10 dígitos.")
        return digitos

    @field_validator("telefono")
    @classmethod
    def _telefono(cls, valor: str) -> str:
        digitos = re.sub(r"\D", "", valor)
        if not 7 <= len(digitos) <= 12:
            raise ValueError("El teléfono debe tener entre 7 y 12 dígitos.")
        return digitos


class Prioridad(BaseModel):
    nombre: Literal[tuple(NIVELES_PRIORIDAD)]
    nivel: int = Field(ge=1, le=3)
    dias_max_respuesta: int = Field(ge=1, le=90)

    @model_validator(mode="after")
    def _nivel_coherente(self):
        if NIVELES_PRIORIDAD[self.nombre] != self.nivel:
            raise ValueError(f"La prioridad {self.nombre} corresponde al nivel {NIVELES_PRIORIDAD[self.nombre]}.")
        return self


class Reto(BaseModel):
    nombre: str = Field(min_length=3, max_length=200)
    descripcion: str = Field(min_length=3, max_length=1000)
    fecha_inicio: date
    fecha_fin: date
    estado: Literal[ESTADOS_RETO]
    id_empresa: Optional[str] = None
    id_categoria: Optional[str] = None
    id_prioridad: Optional[str] = None

    _t = field_validator("nombre", "descripcion")(_texto)

    @model_validator(mode="after")
    def _fechas(self):
        if self.fecha_fin < self.fecha_inicio:
            raise ValueError("La fecha de fin no puede ser anterior a la de inicio.")
        return self


class RegistroParticipacion(BaseModel):
    fecha_registro: datetime
    observacion: str = Field(min_length=1, max_length=1000)
    estado: Literal[ESTADOS_REGISTRO]
    id_usuario: Optional[str] = None
    id_reto: Optional[str] = None

    _t = field_validator("observacion")(_texto)


class Usuario(BaseModel):
    nombre: str = Field(min_length=3, max_length=120)
    correo: str
    rol: Literal[ROLES]
    activo: bool = True
    contrasena: Optional[str] = None  # obligatoria al crear, opcional al editar

    _n = field_validator("nombre")(_texto)
    _c = field_validator("correo")(_correo)
    _p = field_validator("contrasena")(_contrasena)
