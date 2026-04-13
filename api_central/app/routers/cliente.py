from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import bcrypt
from datetime import datetime, timezone
from app.data.database import get_db
from app import models
from app.crud.usuario import get_usuario_by_email

router = APIRouter(prefix="/cliente", tags=["Cliente"])


# ─── Schemas ──────────────────────────────────────────────────────────────────

class RegistroRequest(BaseModel):
    nombre: str
    email: EmailStr
    password: str


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    activo: Optional[bool] = None
    password: Optional[str] = None


class ItemPedido(BaseModel):
    autoparte_id: int
    cantidad: int


class PedidoClienteCreate(BaseModel):
    usuario_id: int
    items: List[ItemPedido]


# ─── Autenticación de cliente ─────────────────────────────────────────────────

@router.post("/token", summary="Login para clientes")
def login_cliente(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    usuario = get_usuario_by_email(db, email=form_data.username)

    if not usuario:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

    if not usuario.activo:
        raise HTTPException(
            status_code=403,
            detail="Tu cuenta está desactivada. Contacta al soporte."
        )

    try:
        password_ok = bcrypt.checkpw(
            form_data.password.encode("utf-8"),
            usuario.password_hash.encode("utf-8"),
        )
    except Exception:
        password_ok = False

    if not password_ok:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

    return {
        "access_token": usuario.email,
        "token_type": "bearer",
        "usuario_id": usuario.id,
        "nombre": usuario.nombre,
        "email": usuario.email,
    }


# ─── CRUD de usuarios externos (rol: Usuario) ─────────────────────────────────

@router.post("/registro", summary="Registrar nuevo usuario externo", status_code=201)
def registro_cliente(data: RegistroRequest, db: Session = Depends(get_db)):
    if get_usuario_by_email(db, email=data.email):
        raise HTTPException(status_code=409, detail="Este correo ya está registrado")

    rol_usuario = (
        db.query(models.Rol)
        .filter(models.Rol.nombre.ilike("usuario"))
        .first()
    )
    if not rol_usuario:
        rol_usuario = models.Rol(nombre="Usuario", descripcion="Usuario cliente de la tienda en línea")
        db.add(rol_usuario)
        db.commit()
        db.refresh(rol_usuario)

    hashed = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    nuevo = models.Usuario(
        nombre=data.nombre,
        email=data.email,
        password_hash=hashed,
        rol_id=rol_usuario.id,
        activo=True,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return {
        "id": nuevo.id,
        "nombre": nuevo.nombre,
        "email": nuevo.email,
        "rol": rol_usuario.nombre,
        "mensaje": "Cuenta creada exitosamente",
    }


@router.get("/usuarios/", summary="Listar usuarios externos")
def listar_clientes(db: Session = Depends(get_db)):
    rol_usuario = (
        db.query(models.Rol)
        .filter(models.Rol.nombre.ilike("usuario"))
        .first()
    )
    if not rol_usuario:
        return []
    usuarios = (
        db.query(models.Usuario)
        .filter(models.Usuario.rol_id == rol_usuario.id)
        .order_by(models.Usuario.id)
        .all()
    )
    return [
        {"id": u.id, "nombre": u.nombre, "email": u.email, "activo": u.activo}
        for u in usuarios
    ]


@router.get("/usuarios/{usuario_id}", summary="Obtener usuario externo por ID")
def obtener_cliente(usuario_id: int, db: Session = Depends(get_db)):
    u = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"id": u.id, "nombre": u.nombre, "email": u.email, "activo": u.activo}


@router.put("/usuarios/{usuario_id}", summary="Actualizar usuario externo")
def actualizar_cliente(usuario_id: int, data: ClienteUpdate, db: Session = Depends(get_db)):
    u = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if data.nombre is not None:
        u.nombre = data.nombre
    if data.email is not None:
        conflicto = db.query(models.Usuario).filter(
            models.Usuario.email == data.email,
            models.Usuario.id != usuario_id,
        ).first()
        if conflicto:
            raise HTTPException(status_code=409, detail="El correo ya está en uso por otro usuario")
        u.email = data.email
    if data.activo is not None:
        u.activo = data.activo
    if data.password is not None:
        u.password_hash = bcrypt.hashpw(
            data.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    db.commit()
    db.refresh(u)
    return {"id": u.id, "nombre": u.nombre, "email": u.email, "activo": u.activo}


@router.delete("/usuarios/{usuario_id}", summary="Eliminar usuario externo")
def eliminar_cliente(usuario_id: int, db: Session = Depends(get_db)):
    u = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    nombre = u.nombre
    db.delete(u)
    db.commit()
    return {"mensaje": f"Usuario '{nombre}' eliminado correctamente"}


# ─── Pedidos del cliente ──────────────────────────────────────────────────────

@router.get("/pedidos/", summary="Pedidos de un usuario específico")
def pedidos_usuario(usuario_id: int, db: Session = Depends(get_db)):
    resultados = (
        db.query(
            models.Pedido.id,
            models.Pedido.fecha_pedido,
            models.Pedido.total,
            models.EstadoPedido.nombre.label("estatus"),
        )
        .join(models.EstadoPedido, models.Pedido.estado_id == models.EstadoPedido.id)
        .filter(models.Pedido.usuario_id == usuario_id)
        .order_by(models.Pedido.id.desc())
        .all()
    )
    return [
        {
            "id": r.id,
            "fecha_pedido": r.fecha_pedido,
            "total": float(r.total),
            "estatus": r.estatus,
        }
        for r in resultados
    ]


@router.post("/pedidos/", summary="Crear pedido desde el carrito del cliente")
def crear_pedido_cliente(pedido: PedidoClienteCreate, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == pedido.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not pedido.items:
        raise HTTPException(status_code=400, detail="El pedido no tiene productos")

    estado_inicial = (
        db.query(models.EstadoPedido)
        .filter(models.EstadoPedido.nombre == "PENDIENTE")
        .first()
    )
    if not estado_inicial:
        raise HTTPException(
            status_code=500,
            detail="El sistema no está inicializado correctamente. Contacta al administrador.",
        )

    total = 0.0
    items_validados = []

    for item in pedido.items:
        autoparte = (
            db.query(models.Autoparte)
            .filter(
                models.Autoparte.id == item.autoparte_id,
                models.Autoparte.activo == True,
            )
            .first()
        )
        if not autoparte:
            raise HTTPException(
                status_code=404,
                detail=f"Producto ID {item.autoparte_id} no disponible",
            )

        inventario = (
            db.query(models.Inventario)
            .filter(models.Inventario.autoparte_id == item.autoparte_id)
            .first()
        )
        stock_disp = inventario.stock_actual if inventario else 0
        if stock_disp < item.cantidad:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente para '{autoparte.nombre}'. Disponible: {stock_disp}",
            )

        precio = float(autoparte.precio)
        total += precio * item.cantidad
        items_validados.append(
            {"autoparte": autoparte, "cantidad": item.cantidad, "precio": precio}
        )

    nuevo_pedido = models.Pedido(
        usuario_id=pedido.usuario_id,
        estado_id=estado_inicial.id,
        fecha_pedido=datetime.now(timezone.utc),
        total=total,
    )
    db.add(nuevo_pedido)
    db.flush()

    for item in items_validados:
        db.add(
            models.DetallePedido(
                pedido_id=nuevo_pedido.id,
                autoparte_id=item["autoparte"].id,
                cantidad=item["cantidad"],
                precio_unitario=item["precio"],
            )
        )

    db.commit()
    db.refresh(nuevo_pedido)

    return {
        "id": nuevo_pedido.id,
        "total": float(nuevo_pedido.total),
        "estatus": estado_inicial.nombre,
        "mensaje": "¡Pedido realizado con éxito!",
    }
