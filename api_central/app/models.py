from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DECIMAL, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import datetime

# Contacto con la BD MySQL por medio de SQLAlchemy
class Rol(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(150))
    
    usuarios = relationship("Usuario", back_populates="rol")

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id"))
    fecha_registro = Column(DateTime, default=func.now())
    activo = Column(Boolean, default=True)
    
    rol = relationship("Rol", back_populates="usuarios")

class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(String(150))
    
    autopartes = relationship("Autoparte", back_populates="categoria")

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

class Inventario(Base):
    __tablename__ = "inventarios"
    id = Column(Integer, primary_key=True, index=True)
    autoparte_id = Column(Integer, ForeignKey("autopartes.id", ondelete="RESTRICT"), unique=True)
    stock_actual = Column(Integer, nullable=False)
    stock_minimo = Column(Integer, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.datetime.utcnow)

    # Relación
    autoparte = relationship("Autoparte")

class EstadoPedido(Base):
    __tablename__ = "estados_pedido"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    # Relación con pedidos
    pedidos = relationship("Pedido", back_populates="estado")

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