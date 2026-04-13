from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import bcrypt
from app.crud.usuario import get_usuario_by_email
from app.data.database import get_db
from app.data.models.rol import Rol as RolModel

router = APIRouter()

@router.get("/", tags=["Inicio"])
async def inicio():
    return {"mensaje": "Bienvenido a la API del proyecto Macuin :)"}

@router.post("/token", tags=["Seguridad"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = get_usuario_by_email(db, email=form_data.username)

    if not usuario:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

    try:
        password_correcta = bcrypt.checkpw(
            form_data.password.encode('utf-8'), 
            usuario.password_hash.encode('utf-8')
        )
    except Exception:
        password_correcta = False

    if not password_correcta:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    # Validación para permitir ingreso al sistema solo de Administradores
    rol_del_usuario = db.query(RolModel).filter(RolModel.id == usuario.rol_id).first()
    
    if not rol_del_usuario or "admin" not in rol_del_usuario.nombre.lower():
        raise HTTPException(
            status_code=403, # 403 significa "Prohibido / Sin Permisos"
            detail="Acceso denegado. Este panel es exclusivo para personal administrativo."
        )

    return {
        "access_token": usuario.email, 
        "token_type": "bearer",
        "nombre": usuario.nombre
    }

@router.get("/roles/", tags=["Usuarios"])
def leer_roles(db: Session = Depends(get_db)):
    return db.query(RolModel).all()