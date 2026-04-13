from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.data.database import Base


class EstadoPedido(Base):
    __tablename__ = "estados_pedido"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    # Relación con pedidos
    pedidos = relationship("Pedido", back_populates="estado")
