from sqlalchemy import Column, Integer, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import relationship
import datetime
from app.data.database import Base


class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="RESTRICT"))
    estado_id = Column(Integer, ForeignKey("estados_pedido.id", ondelete="RESTRICT"))
    fecha_pedido = Column(DateTime, default=datetime.datetime.utcnow)
    total = Column(DECIMAL(10, 2), nullable=False)

    # Relaciones
    usuario = relationship("Usuario")
    estado = relationship("EstadoPedido", back_populates="pedidos")
    detalles = relationship("DetallePedido", back_populates="pedido")
