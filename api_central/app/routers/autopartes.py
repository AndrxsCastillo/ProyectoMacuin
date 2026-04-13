from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.data.database import get_db
from app.data.models.autoparte import Autoparte as AutoparteModel
from app.data.models.inventario import Inventario as InventarioModel
from app.data.models.categoria import Categoria as CategoriaModel  # <-- NUEVO IMPORT
from app.schemas.autoparte import AutoparteCreate, AutoparteUpdate, Autoparte as AutoparteSchema
from app.crud.autoparte import (
    create_autoparte,
    get_autopartes,
    get_autoparte,
    update_autoparte,
    delete_autoparte,
)

router = APIRouter(prefix="/autopartes", tags=["Autopartes"])


@router.post("/", response_model=AutoparteSchema)
def crear_autoparte(autoparte: AutoparteCreate, db: Session = Depends(get_db)):
    return create_autoparte(db=db, autoparte=autoparte)


@router.get("/")
def leer_autopartes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(
        AutoparteModel.id,
        AutoparteModel.nombre,
        AutoparteModel.descripcion,
        AutoparteModel.categoria_id,
        CategoriaModel.nombre.label("categoria_nombre"),
        AutoparteModel.marca,
        AutoparteModel.precio,
        AutoparteModel.activo,
        InventarioModel.stock_actual,
        InventarioModel.stock_minimo,
    ).outerjoin(
        Inventory := InventarioModel, AutoparteModel.id == Inventory.autoparte_id
    ).outerjoin(
        CategoriaModel, AutoparteModel.categoria_id == CategoriaModel.id
    ).order_by(
        AutoparteModel.id  # <--- ESTA ES LA MAGIA QUE CONGELA EL ORDEN
    ).offset(skip).limit(limit)

    piezas_db = query.all()
    lista_piezas = []

    for p in piezas_db:
        lista_piezas.append({
            "id": p.id,
            "nombre": p.nombre,
            "descripcion": p.descripcion,
            "categoria_id": p.categoria_id,
            "categoria_nombre": p.categoria_nombre if p.categoria_nombre else "Sin Categoría", # <-- NUEVO
            "marca": p.marca,
            "precio": float(p.precio),
            "activo": p.activo,
            "stock_actual": p.stock_actual if p.stock_actual is not None else 0,
            "stock_minimo": p.stock_minimo if p.stock_minimo is not None else 0,
        })

    return lista_piezas


@router.get("/{autoparte_id}")
def leer_autoparte(autoparte_id: int, db: Session = Depends(get_db)):
    db_autoparte = get_autoparte(db, autoparte_id=autoparte_id)
    if db_autoparte is None:
        raise HTTPException(status_code=404, detail="Autoparte no encontrada")

    db_inventario = db.query(Inventory := InventarioModel).filter(Inventory.autoparte_id == autoparte_id).first()

    return {
        "id": db_autoparte.id,
        "nombre": db_autoparte.nombre,
        "descripcion": db_autoparte.descripcion,
        "categoria_id": db_autoparte.categoria_id,
        "marca": db_autoparte.marca,
        "precio": float(db_autoparte.precio),
        "activo": db_autoparte.activo,
        "stock_actual": db_inventario.stock_actual if db_inventario else 0,
        "stock_minimo": db_inventario.stock_minimo if db_inventario else 0,
    }


@router.put("/{autoparte_id}", response_model=AutoparteSchema)
def actualizar_autoparte(autoparte_id: int, autoparte: AutoparteUpdate, db: Session = Depends(get_db)):
    db_autoparte = update_autoparte(db, autoparte_id=autoparte_id, autoparte_data=autoparte)
    if db_autoparte is None:
        raise HTTPException(status_code=404, detail="Autoparte no encontrada")
    return db_autoparte


@router.delete("/{autoparte_id}", response_model=AutoparteSchema)
def eliminar_autoparte(autoparte_id: int, db: Session = Depends(get_db)):
    db_autoparte = delete_autoparte(db, autoparte_id=autoparte_id)
    if db_autoparte is None:
        raise HTTPException(status_code=404, detail="Autoparte no encontrada")
    return db_autoparte