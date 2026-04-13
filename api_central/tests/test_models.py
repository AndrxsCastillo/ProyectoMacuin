import decimal
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from app import models
from app.data.database import Base


def _setup_engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return engine


def test_tables_exist():
    engine = _setup_engine()
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    expected = [
        "roles",
        "usuarios",
        "categorias",
        "autopartes",
        "inventarios",
        "estados_pedido",
        "pedidos",
        "detalle_pedido",
    ]

    for t in expected:
        assert t in tables


def test_insert_and_relations():
    engine = _setup_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        # Rol
        rol = models.Rol(nombre="admin", descripcion="Administrador")
        session.add(rol)
        session.commit()
        assert rol.id is not None

        # Usuario
        usuario = models.Usuario(
            nombre="Test User",
            email="test@example.com",
            password_hash="hash",
            rol_id=rol.id,
        )
        session.add(usuario)
        session.commit()
        assert usuario.id is not None
        session.refresh(usuario)
        assert usuario.rol is not None
        assert usuario.rol.nombre == "admin"

        # Categoria + Autoparte + Inventario
        categoria = models.Categoria(nombre="Motores", descripcion="Cat Motores")
        session.add(categoria)
        session.commit()

        autoparte = models.Autoparte(
            nombre="Filtro",
            descripcion="Filtro de aceite",
            categoria_id=categoria.id,
            marca="MarcaX",
            precio=decimal.Decimal("12.34"),
        )
        session.add(autoparte)
        session.commit()
        assert autoparte.id is not None

        inventario = models.Inventario(autoparte_id=autoparte.id, stock_actual=10, stock_minimo=2)
        session.add(inventario)
        session.commit()

        session.refresh(autoparte)
        assert getattr(autoparte, "inventario") is not None
        assert autoparte.inventario.stock_actual == 10

        # Pedido y detalle
        estado = models.EstadoPedido(nombre="pendiente")
        session.add(estado)
        session.commit()

        pedido = models.Pedido(usuario_id=usuario.id, estado_id=estado.id, total=decimal.Decimal("100.00"))
        session.add(pedido)
        session.commit()
        assert pedido.id is not None

        detalle = models.DetallePedido(pedido_id=pedido.id, autoparte_id=autoparte.id, cantidad=2, precio_unitario=decimal.Decimal("12.34"))
        session.add(detalle)
        session.commit()

        session.refresh(pedido)
        assert len(pedido.detalles) == 1

    finally:
        session.close()
