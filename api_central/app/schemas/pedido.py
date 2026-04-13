from pydantic import BaseModel
from datetime import datetime


class PedidoActualizarEstatus(BaseModel):
    estatus: str


class PedidoBase(BaseModel):
    id: int
    fecha_pedido: datetime
    total: float
    estatus: str # Aquí enviaremos el nombre del estado, no el ID

    class Config:
        from_attributes = True
