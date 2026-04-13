from pydantic import BaseModel
from typing import Optional


class RolBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class Rol(RolBase):
    id: int

    class Config:
        from_attributes = True
