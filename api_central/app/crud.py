from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas
import bcrypt

# ==========================================
# MOTOR DE ENCRIPTACIÓN NATIVO (Sin Passlib)
# ==========================================
def get_password_hash(password: str):
    # 1. Convertimos el texto a bytes
    pwd_bytes = password.encode('utf-8')
    # 2. Generamos una "sal" aleatoria para mayor seguridad
    salt = bcrypt.gensalt()
    # 3. Encriptamos la contraseña
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    # 4. La devolvemos como texto normal para guardarla en MySQL
    return hashed_password.decode('utf-8')

# ==========================================
# CRUD PARA USUARIOS
# ==========================================
def get_usuario(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

def get_usuario_by_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Usuario).offset(skip).limit(limit).all()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    # Encriptamos la contraseña antes de guardar
    hashed_password = get_password_hash(usuario.password)
    
    db_usuario = models.Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        password_hash=hashed_password,
        rol_id=usuario.rol_id,
        activo=usuario.activo
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db: Session, usuario_id: int, usuario_data: schemas.UsuarioUpdate):
    db_usuario = get_usuario(db, usuario_id)
    if not db_usuario:
        return None
    
    update_data = usuario_data.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))
        
    for key, value in update_data.items():
        setattr(db_usuario, key, value)
        
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id: int):
    db_usuario = get_usuario(db, usuario_id)
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
    return db_usuario

# ==========================================
# CRUD PARA AUTOPARTES Y PRODUCTOS
# ==========================================
def get_autoparte(db: Session, autoparte_id: int):
    return db.query(models.Autoparte).filter(models.Autoparte.id == autoparte_id).first()

def get_autopartes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Autoparte).offset(skip).limit(limit).all()

def create_autoparte(db: Session, autoparte: schemas.AutoparteCreate):
    # 1. Creamos primero la autoparte
    db_autoparte = models.Autoparte(
        nombre=autoparte.nombre,
        descripcion=autoparte.descripcion,
        categoria_id=autoparte.categoria_id,
        marca=autoparte.marca,
        precio=autoparte.precio,
        activo=autoparte.activo
    )
    db.add(db_autoparte)
    db.commit()
    db.refresh(db_autoparte)
    
    # 2. Con el ID generado de la autoparte, creamos su inventario
    db_inventario = models.Inventario(
        autoparte_id=db_autoparte.id,
        stock_actual=autoparte.stock_inicial,
        stock_minimo=autoparte.stock_minimo
    )
    db.add(db_inventario)
    db.commit()
    
    return db_autoparte

def update_autoparte(db: Session, autoparte_id: int, autoparte_data: schemas.AutoparteUpdate):
    db_autoparte = get_autoparte(db, autoparte_id)
    if not db_autoparte:
        return None
        
    # Convertimos los datos del esquema a diccionario
    update_data = autoparte_data.dict(exclude_unset=True)
    
    # 1. Extraemos y quitamos los datos de inventario para que no rompan el setattr de Autoparte
    stock_actual = update_data.pop("stock_actual", None)
    stock_minimo = update_data.pop("stock_minimo", None)
    
    # 2. Actualizamos dinámicamente solo los campos que pertenecen a la tabla autopartes
    for key, value in update_data.items():
        setattr(db_autoparte, key, value)
        
    # 3. Actualizamos o creamos el registro en la tabla inventarios
    if stock_actual is not None and stock_minimo is not None:
        # Buscamos si ya tiene un inventario registrado
        db_inventario = db.query(models.Inventario).filter(models.Inventario.autoparte_id == autoparte_id).first()
        
        if db_inventario:
            # Si existe, lo actualizamos
            db_inventario.stock_actual = stock_actual
            db_inventario.stock_minimo = stock_minimo
        else:
            # Si no existe (porque lo insertaste manual y se te pasó), lo creamos
            nuevo_inventario = models.Inventario(
                autoparte_id=autoparte_id,
                stock_actual=stock_actual,
                stock_minimo=stock_minimo
            )
            db.add(nuevo_inventario)
            
    # 4. Guardamos todos los cambios (autopartes e inventarios) al mismo tiempo
    db.commit()
    db.refresh(db_autoparte)
    
    return db_autoparte

def delete_autoparte(db: Session, autoparte_id: int):
    db_autoparte = get_autoparte(db, autoparte_id)
    if db_autoparte:
        # Por la restricción de llaves foráneas, primero borramos el inventario
        db_inventario = db.query(models.Inventario).filter(models.Inventario.autoparte_id == autoparte_id).first()
        if db_inventario:
            db.delete(db_inventario)
            
        db.delete(db_autoparte)
        db.commit()
    return db_autoparte

# ==========================================
# CRUD PARA CATEGORÍAS
# ==========================================
def get_categorias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Categoria).offset(skip).limit(limit).all()