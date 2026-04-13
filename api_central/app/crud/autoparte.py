from sqlalchemy.orm import Session
from app.data.models.autoparte import Autoparte as AutoparteModel
from app.data.models.inventario import Inventario as InventarioModel
from app.schemas.autoparte import AutoparteCreate, AutoparteUpdate


# ==========================================
# CRUD PARA AUTOPARTES Y PRODUCTOS
# ==========================================
def get_autoparte(db: Session, autoparte_id: int):
    return db.query(AutoparteModel).filter(AutoparteModel.id == autoparte_id).first()


def get_autopartes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AutoparteModel).offset(skip).limit(limit).all()


def create_autoparte(db: Session, autoparte: AutoparteCreate):
    db_autoparte = AutoparteModel(
        nombre=autoparte.nombre,
        descripcion=autoparte.descripcion,
        categoria_id=autoparte.categoria_id,
        marca=autoparte.marca,
        precio=autoparte.precio,
        activo=autoparte.activo,
    )
    db.add(db_autoparte)
    db.commit()
    db.refresh(db_autoparte)

    db_inventario = InventarioModel(
        autoparte_id=db_autoparte.id,
        stock_actual=autoparte.stock_inicial,
        stock_minimo=autoparte.stock_minimo,
    )
    db.add(db_inventario)
    db.commit()

    return db_autoparte


def update_autoparte(db: Session, autoparte_id: int, autoparte_data: AutoparteUpdate):
    db_autoparte = get_autoparte(db, autoparte_id)
    if not db_autoparte:
        return None

    update_data = autoparte_data.dict(exclude_unset=True)

    stock_actual = update_data.pop("stock_actual", None)
    stock_minimo = update_data.pop("stock_minimo", None)

    for key, value in update_data.items():
        setattr(db_autoparte, key, value)

    if stock_actual is not None and stock_minimo is not None:
        db_inventario = db.query(InventarioModel).filter(InventarioModel.autoparte_id == autoparte_id).first()

        if db_inventario:
            db_inventario.stock_actual = stock_actual
            db_inventario.stock_minimo = stock_minimo
        else:
            nuevo_inventario = InventarioModel(
                autoparte_id=autoparte_id,
                stock_actual=stock_actual,
                stock_minimo=stock_minimo,
            )
            db.add(nuevo_inventario)

    db.commit()
    db.refresh(db_autoparte)

    return db_autoparte


def delete_autoparte(db: Session, autoparte_id: int):
    db_autoparte = get_autoparte(db, autoparte_id)
    if db_autoparte:
        db_inventario = db.query(InventarioModel).filter(InventarioModel.autoparte_id == autoparte_id).first()
        if db_inventario:
            db.delete(db_inventario)

        db.delete(db_autoparte)
        db.commit()
    return db_autoparte
