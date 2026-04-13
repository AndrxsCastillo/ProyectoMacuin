from sqlalchemy.orm import Session
from app.data.models.categoria import Categoria as CategoriaModel


# ==========================================
# CRUD PARA CATEGORÍAS
# ==========================================
def get_categorias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CategoriaModel).offset(skip).limit(limit).all()
