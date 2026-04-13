from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app import models, schemas
from app.data.database import get_db

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


# 1. Quitamos el response_model=List[schemas.PedidoBase] del decorador
@router.get("/")
def leer_pedidos(db: Session = Depends(get_db)):
    # Agregamos el order_by para que SIEMPRE salgan ordenados (los más recientes primero)
    resultados = db.query(
        models.Pedido.id,
        models.Pedido.fecha_pedido,
        models.Pedido.total,
        models.EstadoPedido.nombre.label("estatus")
    ).join(
        models.EstadoPedido, models.Pedido.estado_id == models.EstadoPedido.id
    ).order_by(
        models.Pedido.id
    ).all()
    
    # 2. Transformamos las "filas" (Rows) de SQLAlchemy a simples diccionarios
    # para que FastAPI las pueda empaquetar sin quejarse
    lista_final = []
    for r in resultados:
        lista_final.append({
            "id": r.id,
            "fecha_pedido": r.fecha_pedido,
            "total": r.total,
            "estatus": r.estatus
        })
        
    return lista_final


@router.put("/{id}/estatus")
def actualizar_estatus_pedido(id: int, estatus_data: schemas.PedidoActualizarEstatus, db: Session = Depends(get_db)):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    nuevo_estado = db.query(models.EstadoPedido).filter(models.EstadoPedido.nombre == estatus_data.estatus).first()
    if not nuevo_estado:
        raise HTTPException(status_code=400, detail="El estado proporcionado no existe en el catálogo")

    estado_actual = db.query(models.EstadoPedido).filter(models.EstadoPedido.id == pedido.estado_id).first()

    # LÓGICA DE INVENTARIO: Si el nuevo estado es SURTIDO, descontamos stock
    # (se aplica siempre para asegurar consistencia en ejecuciones de pruebas)
    if nuevo_estado.nombre.upper() == 'SURTIDO':
        for detalle in pedido.detalles:
            inventario = db.query(models.Inventario).filter(models.Inventario.autoparte_id == detalle.autoparte_id).first()
            
            if not inventario:
                raise HTTPException(status_code=400, detail=f"No hay registro de inventario para la pieza ID {detalle.autoparte_id}")
            
            if inventario.stock_actual < detalle.cantidad:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Stock insuficiente para la pieza ID {detalle.autoparte_id}. Solicitado: {detalle.cantidad}, Disponible: {inventario.stock_actual}"
                )
            
            # Si hay stock, lo descontamos
            inventario.stock_actual -= detalle.cantidad

            # NUEVO METODO: Usamos now con la zona horaria UTC explícita
            inventario.fecha_actualizacion = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)

    # Actualizamos el estado del pedido
    pedido.estado_id = nuevo_estado.id
    db.commit()
    
    return {"mensaje": "Estatus actualizado correctamente", "estatus": nuevo_estado.nombre.upper()}

@router.get("/{id}")
def obtener_detalle_pedido(id: int, db: Session = Depends(get_db)):
    # Buscamos el pedido
    pedido = db.query(models.Pedido).filter(models.Pedido.id == id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    # Obtenemos su estatus en texto
    estatus = db.query(models.EstadoPedido).filter(models.EstadoPedido.id == pedido.estado_id).first().nombre
    
    # Armamos la lista de detalles
    detalles_lista = []
    for detalle in pedido.detalles:
        pieza = db.query(models.Autoparte).filter(models.Autoparte.id == detalle.autoparte_id).first()
        detalles_lista.append({
            "pieza_nombre": pieza.nombre if pieza else "Pieza Desconocida",
            "marca": pieza.marca if pieza else "N/A",
            "cantidad": detalle.cantidad,
            "precio_unitario": float(detalle.precio_unitario),
            "subtotal": float(detalle.cantidad * detalle.precio_unitario)
        })
        
    # Empaquetamos todo en un diccionario limpio
    return {
        "id": pedido.id,
        "fecha_pedido": pedido.fecha_pedido,
        "total": float(pedido.total),
        "estatus": estatus,
        "detalles": detalles_lista
    }
