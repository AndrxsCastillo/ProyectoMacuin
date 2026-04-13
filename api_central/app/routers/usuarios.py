from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.data.database import get_db
from app.data.models.usuario import Usuario as UsuarioModel
from app.data.models.rol import Rol as RolModel
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, Usuario as UsuarioSchema
from app.crud.usuario import (
    get_usuario,
    get_usuario_by_email,
    create_usuario,
    update_usuario,
    delete_usuario,
    get_usuarios,
)

router = APIRouter(prefix="/usuarios", tags=["Administradores"])


@router.post("/", response_model=UsuarioSchema, status_code=201)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if get_usuario_by_email(db, email=usuario.email):
        raise HTTPException(status_code=409, detail="Ya existe un usuario registrado con ese correo")
    return create_usuario(db=db, usuario=usuario)


@router.get("/")
def leer_usuarios(db: Session = Depends(get_db)):
    # AQUÍ APLICAMOS LA MAGIA: Agregamos .order_by(UsuarioModel.id) antes del .all()
    usuarios_db = db.query(UsuarioModel).order_by(UsuarioModel.id).all()
    lista_usuarios = []

    for u in usuarios_db:
        rol_db = db.query(RolModel).filter(RolModel.id == u.rol_id).first()
        nombre_rol = rol_db.nombre if rol_db else "Sin Rol"

        lista_usuarios.append({
            "id": u.id,
            "nombre": u.nombre,
            "email": u.email,
            "activo": u.activo,
            "rol": nombre_rol,
        })

    return lista_usuarios


@router.put("/{usuario_id}", response_model=UsuarioSchema)
def actualizar_usuario(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    db_usuario = update_usuario(db, usuario_id=usuario_id, usuario_data=usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario


@router.delete("/{usuario_id}", response_model=UsuarioSchema)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = delete_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario
