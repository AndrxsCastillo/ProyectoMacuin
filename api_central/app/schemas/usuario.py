from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr  # Valida automáticamente que sea un correo real
    rol_id: int
    activo: Optional[bool] = True


class UsuarioCreate(UsuarioBase):
    password: str  # Solo se pide al crear, nunca se devuelve en la respuesta


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    rol_id: Optional[int] = None
    activo: Optional[bool] = None
    password: Optional[str] = None


class Usuario(UsuarioBase):
    id: int
    fecha_registro: datetime

    class Config:
        from_attributes = True  # Permite leer datos desde modelos de SQLAlchemy
