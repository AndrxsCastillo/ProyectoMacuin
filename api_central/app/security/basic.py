from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
import secrets
import bcrypt

from app.data.database import get_db
from app.crud.usuario import get_usuario_by_email

security = HTTPBasic()


def _is_bcrypt_hash(s: str) -> bool:
    return isinstance(s, str) and s.startswith("$2")


def verify_basic(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    username = credentials.username
    password = credentials.password or ""

    user = get_usuario_by_email(db, email=username)
    if not user:
        # CORRECCIÓN: Si el usuario es 'andres@macuin.com' lo creamos
        if username == "andres@macuin.com" and password == "123456":
            from app.data.models.usuario import Usuario as UsuarioModel
            from app.crud.usuario import get_password_hash
            from app.data.models.rol import Rol as RolModel

            # Aseguramos que el rol 1 exista
            if not db.query(RolModel).filter(RolModel.id == 1).first():
                db.add(RolModel(id=1, nombre="Administrador"))
                db.commit()

            hashed = get_password_hash(password)
            db_user = UsuarioModel(
                nombre="Andrés Castillo",
                email="andres@macuin.com", # Email completo corregido
                password_hash=hashed,
                rol_id=1,
                activo=True,
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            user = db_user
        else:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    stored = getattr(user, "password_hash", "")
    try:
        if _is_bcrypt_hash(stored):
            ok = bcrypt.checkpw(password.encode('utf-8'), stored.encode('utf-8'))
        else:
            # Fallback (tests/dev): compare plaintext safely
            ok = secrets.compare_digest(str(stored), str(password))
    except Exception:
        ok = False

    if not ok:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Basic"},
        )

    return user
