from pydantic import BaseModel
from typing import Optional


class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class CategoriaCreate(CategoriaBase):
    pass


class Categoria(CategoriaBase):
    id: int

    class Config:
        from_attributes = True
