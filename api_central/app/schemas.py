from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# ==========================================
# SCHEMAS PARA TOKENS (Seguridad)
# ==========================================
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# ==========================================
# SCHEMAS PARA ROLES
# ==========================================
class RolBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class Rol(RolBase):
    id: int

    class Config:
        from_attributes = True

# ==========================================
# SCHEMAS PARA USUARIOS (CRUD Completo)
# ==========================================
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

# ==========================================
# SCHEMAS PARA CATEGORÍAS
# ==========================================
class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int

    class Config:
        from_attributes = True

# ==========================================
# SCHEMAS PARA AUTOPARTES Y PRODUCTOS
# ==========================================
class AutoparteBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    categoria_id: int
    marca: Optional[str] = None
    precio: Decimal = Field(..., ge=0)  # ge=0 asegura que el precio sea mayor o igual a 0
    activo: Optional[bool] = True

class AutoparteCreate(AutoparteBase):
    # Pedimos el stock inicial de una vez para crear su registro en la tabla inventarios
    stock_inicial: int = Field(default=0, ge=0)
    stock_minimo: int = Field(default=5, ge=0)

class AutoparteUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    categoria_id: Optional[int] = None
    marca: Optional[str] = None
    precio: Optional[Decimal] = Field(None, ge=0)
    activo: Optional[bool] = None

class Autoparte(AutoparteBase):
    id: int

    class Config:
        from_attributes = True


# Esquema para recibir el nuevo estatus desde Flask
class PedidoActualizarEstatus(BaseModel):
    estatus: str


class PedidoBase(BaseModel):
    id: int
    fecha_pedido: datetime
    total: float
    estatus: str # Aquí enviaremos el nombre del estado, no el ID

    class Config:
        from_attributes = True