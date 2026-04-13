from fastapi import APIRouter, Depends, Query, HTTPException
from app.services.report_generator import generar_archivo
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.data.database import get_db
from app.data.models.autoparte import Autoparte as AutoparteModel
from app.data.models.inventario import Inventario as InventarioModel
from app.data.models.categoria import Categoria as CategoriaModel
from app.data.models.pedido import Pedido as PedidoModel
from app.data.models.estado_pedido import EstadoPedido as EstadoPedidoModel
from app.data.models.detalle_pedido import DetallePedido as DetallePedidoModel
from app.data.models.usuario import Usuario as UsuarioModel
from app.data.models.rol import Rol as RolModel
from datetime import datetime

router = APIRouter(prefix="/reportes", tags=["Reportes"])


# ─── Dashboard (métricas en tiempo real) ─────────────────────────────────────

@router.get("/", summary="Métricas del dashboard de reportes")
def obtener_reportes(db: Session = Depends(get_db)):
    ingresos_totales = db.query(func.sum(PedidoModel.total)).scalar() or 0.0

    pedidos_por_estatus = db.query(
        EstadoPedidoModel.nombre.label("estatus"),
        func.count(PedidoModel.id).label("cantidad"),
    ).outerjoin(PedidoModel, EstadoPedidoModel.id == PedidoModel.estado_id).group_by(EstadoPedidoModel.nombre).all()
    resumen_pedidos = {item.estatus: item.cantidad for item in pedidos_por_estatus}

    inventario_bajo = db.query(
        AutoparteModel.nombre, InventarioModel.stock_actual, InventarioModel.stock_minimo,
    ).join(InventarioModel, InventarioModel.autoparte_id == AutoparteModel.id).filter(
        InventarioModel.stock_actual <= InventarioModel.stock_minimo
    ).limit(5).all()
    alertas_stock = [{"pieza": i.nombre, "stock_actual": i.stock_actual, "stock_minimo": i.stock_minimo} for i in inventario_bajo]

    top_clientes = db.query(
        UsuarioModel.nombre,
        UsuarioModel.email,
        func.count(PedidoModel.id).label("total_pedidos"),
        func.sum(PedidoModel.total).label("total_comprado"),
    ).join(PedidoModel).group_by(UsuarioModel.id).order_by(func.sum(PedidoModel.total).desc()).limit(5).all()
    reporte_clientes = [{"nombre": c.nombre, "email": c.email, "pedidos": c.total_pedidos, "inversion": float(c.total_comprado)} for c in top_clientes]

    top_ventas = db.query(
        AutoparteModel.nombre,
        func.sum(DetallePedidoModel.cantidad).label("piezas_vendidas"),
        func.sum(DetallePedidoModel.cantidad * DetallePedidoModel.precio_unitario).label("ingreso_generado"),
    ).join(DetallePedidoModel).group_by(AutoparteModel.id).order_by(func.sum(DetallePedidoModel.cantidad).desc()).limit(5).all()
    reporte_ventas = [{"pieza": v.nombre, "vendidas": v.piezas_vendidas, "ingreso": float(v.ingreso_generado)} for v in top_ventas]

    return {
        "ingresos_totales": float(ingresos_totales),
        "resumen_pedidos": resumen_pedidos,
        "alertas_stock": alertas_stock,
        "reporte_clientes": reporte_clientes,
        "reporte_ventas": reporte_ventas,
    }


# ─── Reporte 1: Inventario ────────────────────────────────────────────────────

@router.get("/inventario", summary="Descargar reporte de inventario (PDF/XLSX/DOCX)")
def reporte_inventario(
    formato: str = Query("pdf", description="Formato de descarga: pdf, xlsx, docx"),
    categoria: str = Query(None, description="Filtrar por categoría (opcional)"),
    db: Session = Depends(get_db),
):
    titulo = "Catálogo de Inventario MACUIN"
    columnas = ["#", "Nombre", "Marca", "Categoría", "Stock Actual", "Precio"]

    query = db.query(
        AutoparteModel.id,
        AutoparteModel.nombre,
        AutoparteModel.marca,
        CategoriaModel.nombre.label("categoria_nombre"),
        InventarioModel.stock_actual,
        AutoparteModel.precio,
    ).join(CategoriaModel).outerjoin(InventarioModel).order_by(AutoparteModel.id)

    datos_matriz = []
    contador = 1
    sustituciones = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u"}

    for p in query.all():
        if categoria and categoria != "todas":
            cat_db = str(p.categoria_nombre).lower().replace(" ", "")
            cat_filtro = str(categoria).lower().replace(" ", "")
            for acento, normal in sustituciones.items():
                cat_db = cat_db.replace(acento, normal)
                cat_filtro = cat_filtro.replace(acento, normal)
            if cat_filtro not in cat_db:
                continue

        stock = p.stock_actual if p.stock_actual is not None else 0
        datos_matriz.append([contador, p.nombre, p.marca, p.categoria_nombre, stock, f"${p.precio:.2f}"])
        contador += 1

    if not datos_matriz:
        datos_matriz.append(["-", "Sin resultados", "-", "-", "-", "-"])

    return generar_archivo(formato, titulo, columnas, datos_matriz)


# ─── Reporte 2: Usuarios ──────────────────────────────────────────────────────

@router.get("/usuarios", summary="Descargar reporte de usuarios del sistema (PDF/XLSX/DOCX)")
def reporte_usuarios(
    formato: str = Query("pdf", description="Formato de descarga: pdf, xlsx, docx"),
    rol: str = Query(None, description="Filtrar por rol (opcional)"),
    db: Session = Depends(get_db),
):
    titulo = "Directorio de Usuarios del Sistema"
    columnas = ["#", "Nombre", "Email", "Rol", "Estado"]

    query = db.query(
        UsuarioModel.nombre,
        UsuarioModel.email,
        RolModel.nombre.label("rol_nombre"),
        UsuarioModel.activo,
    ).join(RolModel).order_by(UsuarioModel.id)

    datos_matriz = []
    contador = 1

    for u in query.all():
        if rol and rol != "todos":
            rol_db = str(u.rol_nombre).lower().replace(" ", "")
            rol_filtro = str(rol).lower().replace(" ", "")
            if rol_filtro == "cliente":
                rol_filtro = "usuario"
            if rol_filtro not in rol_db:
                continue

        estado = "Activo" if u.activo else "Inactivo"
        datos_matriz.append([contador, u.nombre, u.email, u.rol_nombre, estado])
        contador += 1

    if not datos_matriz:
        datos_matriz.append(["-", "Sin resultados", "-", "-", "-"])

    return generar_archivo(formato, titulo, columnas, datos_matriz)


# ─── Reporte 3: Alertas de stock crítico ─────────────────────────────────────

@router.get("/alertas", summary="Descargar reporte de alertas de stock crítico (PDF/XLSX/DOCX)")
def reporte_alertas(
    formato: str = Query("pdf", description="Formato de descarga: pdf, xlsx, docx"),
    db: Session = Depends(get_db),
):
    titulo = "Reporte de Stock Crítico (Urgente)"
    columnas = ["#", "Pieza", "Marca", "Stock Actual", "Mínimo Permitido"]

    piezas_criticas = db.query(
        AutoparteModel.nombre,
        AutoparteModel.marca,
        InventarioModel.stock_actual,
        InventarioModel.stock_minimo,
    ).join(InventarioModel).filter(
        InventarioModel.stock_actual <= InventarioModel.stock_minimo
    ).all()

    datos_matriz = []
    for i, p in enumerate(piezas_criticas, start=1):
        datos_matriz.append([i, p.nombre, p.marca, p.stock_actual, p.stock_minimo])

    if not datos_matriz:
        datos_matriz.append(["-", "Sin alertas críticas", "-", "-", "-"])

    return generar_archivo(formato, titulo, columnas, datos_matriz)


# ─── Reporte 4: Ventas / Historial de pedidos ────────────────────────────────

@router.get("/ventas", summary="Descargar reporte de historial de ventas (PDF/XLSX/DOCX)")
def reporte_ventas(
    formato: str = Query("pdf", description="Formato de descarga: pdf, xlsx, docx"),
    fecha_inicio: str = Query(None, description="Fecha inicio filtro (YYYY-MM-DD)"),
    fecha_fin: str = Query(None, description="Fecha fin filtro (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    inicio_fmt = datetime.strptime(fecha_inicio, "%Y-%m-%d").strftime("%d-%m-%Y") if fecha_inicio else "Inicio"
    fin_fmt = datetime.strptime(fecha_fin, "%Y-%m-%d").strftime("%d-%m-%Y") if fecha_fin else "Fin"
    titulo = f"Historial de Ventas ({inicio_fmt} a {fin_fmt})"
    columnas = ["ID Pedido", "Fecha", "Estatus", "Total"]

    query = db.query(
        PedidoModel.id,
        PedidoModel.fecha_pedido,
        EstadoPedidoModel.nombre.label("estatus"),
        PedidoModel.total,
    ).join(EstadoPedidoModel)

    if fecha_inicio and fecha_fin:
        inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
        query = query.filter(
            PedidoModel.fecha_pedido >= inicio_dt,
            PedidoModel.fecha_pedido <= fin_dt,
        )

    query = query.order_by(PedidoModel.id)

    datos_matriz = []
    for p in query.all():
        fecha_str = p.fecha_pedido.strftime("%d-%m-%Y") if p.fecha_pedido else "N/A"
        datos_matriz.append([p.id, fecha_str, p.estatus, f"${p.total:.2f}"])

    if not datos_matriz:
        datos_matriz.append(["-", "Sin ventas", "en el período", "-"])

    return generar_archivo(formato, titulo, columnas, datos_matriz)
