from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.data.database import Base


class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(String(150))
    
    autopartes = relationship("Autoparte", back_populates="categoria")
