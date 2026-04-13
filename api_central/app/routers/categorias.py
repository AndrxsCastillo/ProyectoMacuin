from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from app import schemas, crud
from app.data.database import get_db

router = APIRouter(prefix="/categorias", tags=["Categorías"])


@router.get("/", response_model=List[schemas.Categoria])
def leer_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categorias = crud.get_categorias(db, skip=skip, limit=limit)
    return categorias
