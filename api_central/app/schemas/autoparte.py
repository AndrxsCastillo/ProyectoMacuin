from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


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
    stock_actual: int
    stock_minimo: int
    activo: Optional[bool] = None


class Autoparte(AutoparteBase):
    id: int

    class Config:
        from_attributes = True
