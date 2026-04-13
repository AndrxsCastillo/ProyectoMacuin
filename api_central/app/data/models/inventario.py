from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from app.data.database import Base


class Inventario(Base):
    __tablename__ = "inventarios"
    id = Column(Integer, primary_key=True, index=True)
    autoparte_id = Column(Integer, ForeignKey("autopartes.id", ondelete="RESTRICT"), unique=True)
    stock_actual = Column(Integer, nullable=False)
    stock_minimo = Column(Integer, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.datetime.utcnow)

    # Relación
    autoparte = relationship("Autoparte", back_populates="inventario")
