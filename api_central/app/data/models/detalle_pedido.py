from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from app.data.database import Base


class DetallePedido(Base):
    __tablename__ = "detalle_pedido"
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id", ondelete="CASCADE"))
    autoparte_id = Column(Integer, ForeignKey("autopartes.id", ondelete="RESTRICT"))
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(DECIMAL(10, 2), nullable=False)

    # Relaciones
    pedido = relationship("Pedido", back_populates="detalles")
    autoparte = relationship("Autoparte")
