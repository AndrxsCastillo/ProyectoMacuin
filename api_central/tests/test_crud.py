import decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models, schemas, crud
from app.data.database import Base


def _setup_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return Session


def test_crud_usuario():
    Session = _setup_session()
    db = Session()
    try:
        # Crear rol
        rol = models.Rol(nombre="admin", descripcion="Administrador")
        db.add(rol)
        db.commit()
        db.refresh(rol)

        # Crear usuario via CRUD
        usuario_in = schemas.UsuarioCreate(nombre="Alice", email="alice@example.com", password="secret", rol_id=rol.id)
        usuario = crud.create_usuario(db, usuario=usuario_in)
        assert usuario.id is not None
        assert usuario.email == "alice@example.com"

        # Obtener por email
        fetched = crud.get_usuario_by_email(db, email="alice@example.com")
        assert fetched.id == usuario.id

        # Actualizar
        update = schemas.UsuarioUpdate(nombre="Alice2")
        updated = crud.update_usuario(db, usuario_id=usuario.id, usuario_data=update)
        assert updated.nombre == "Alice2"

        # Eliminar
        deleted = crud.delete_usuario(db, usuario_id=usuario.id)
        assert deleted.id == usuario.id

    finally:
        db.close()


def test_crud_autoparte():
    Session = _setup_session()
    db = Session()
    try:
        # Crear categoria
        categoria = models.Categoria(nombre="Motores", descripcion="Cat Motores")
        db.add(categoria)
        db.commit()
        db.refresh(categoria)

        # Crear autoparte
        ap_in = schemas.AutoparteCreate(
            nombre="Filtro",
            descripcion="Filtro de aceite",
            categoria_id=categoria.id,
            marca="MarcaX",
            precio=decimal.Decimal("12.34"),
            activo=True,
            stock_inicial=5,
            stock_minimo=1,
        )
        ap = crud.create_autoparte(db, autoparte=ap_in)
        assert ap.id is not None

        # Obtener autoparte
        fetched = crud.get_autoparte(db, autoparte_id=ap.id)
        assert fetched.id == ap.id

        # Actualizar inventario via update_autoparte
        up_in = schemas.AutoparteUpdate(stock_actual=10, stock_minimo=2)
        updated = crud.update_autoparte(db, autoparte_id=ap.id, autoparte_data=up_in)
        inv = db.query(models.Inventario).filter(models.Inventario.autoparte_id == ap.id).first()
        assert inv.stock_actual == 10

        # Delete
        deleted = crud.delete_autoparte(db, autoparte_id=ap.id)
        assert deleted.id == ap.id

    finally:
        db.close()
