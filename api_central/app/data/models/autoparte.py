from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.data.database import Base


class Autoparte(Base):
    __tablename__ = "autopartes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    marca = Column(String(100))
    precio = Column(DECIMAL(10, 2), nullable=False)
    activo = Column(Boolean, default=True)
    
    categoria = relationship("Categoria", back_populates="autopartes")
    inventario = relationship("Inventario", back_populates="autoparte", uselist=False)
