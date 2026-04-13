import os
import decimal
from fastapi.testclient import TestClient

# Ensure the app uses the test sqlite DB before importing app
os.environ["DATABASE_URL"] = "sqlite:///./test_api.db"

from app.main import app
from app.data.database import engine, Base, SessionLocal
from app import models
from app.crud.usuario import get_password_hash

client = TestClient(app)


def setup_module(module):
    Base.metadata.create_all(bind=engine)


def teardown_module(module):
    try:
        engine.dispose()
    except Exception:
        pass
    # Keep DB file to avoid race conditions across test modules
    pass


def seed_data():
    db = SessionLocal()
    try:
        rol = db.query(models.Rol).filter(models.Rol.nombre == "admin").first()
        if not rol:
            rol = models.Rol(nombre="admin", descripcion="Admin")
            db.add(rol)
            db.commit()
            db.refresh(rol)

        cat = db.query(models.Categoria).filter(models.Categoria.nombre == "Motores").first()
        if not cat:
            cat = models.Categoria(nombre="Motores", descripcion="Cat Motores")
            db.add(cat)
            db.commit()
            db.refresh(cat)

        ap = db.query(models.Autoparte).filter(models.Autoparte.nombre == "Filtro").first()
        if not ap:
            ap = models.Autoparte(
                nombre="Filtro",
                descripcion="Filtro de aceite",
                categoria_id=cat.id,
                marca="MarcaX",
                precio=decimal.Decimal("12.34"),
                activo=True,
            )
            db.add(ap)
            db.commit()
            db.refresh(ap)
            inv = models.Inventario(autoparte_id=ap.id, stock_actual=10, stock_minimo=1)
            db.add(inv)
            db.commit()
        else:
            inv = db.query(models.Inventario).filter(models.Inventario.autoparte_id == ap.id).first()
            if not inv:
                inv = models.Inventario(autoparte_id=ap.id, stock_actual=10, stock_minimo=1)
                db.add(inv)
                db.commit()

        estado_pend = db.query(models.EstadoPedido).filter(models.EstadoPedido.nombre == "PENDIENTE").first()
        if not estado_pend:
            estado_pend = models.EstadoPedido(nombre="PENDIENTE")
            db.add(estado_pend)
            db.commit()
            db.refresh(estado_pend)

        estado_surtido = db.query(models.EstadoPedido).filter(models.EstadoPedido.nombre == "SURTIDO").first()
        if not estado_surtido:
            estado_surtido = models.EstadoPedido(nombre="SURTIDO")
            db.add(estado_surtido)
            db.commit()
            db.refresh(estado_surtido)

        usuario = db.query(models.Usuario).filter(models.Usuario.email == "report@test").first()
        if not usuario:
            usuario = models.Usuario(nombre="ReportUser", email="report@test", password_hash=get_password_hash("pwd"), rol_id=rol.id)
            db.add(usuario)
            db.commit()
            db.refresh(usuario)
        else:
            usuario.password_hash = get_password_hash("pwd")
            db.add(usuario)
            db.commit()
            db.refresh(usuario)

        pedido = db.query(models.Pedido).filter(models.Pedido.usuario_id == usuario.id).first()
        if not pedido:
            pedido = models.Pedido(usuario_id=usuario.id, estado_id=estado_pend.id, total=decimal.Decimal("24.68"))
            db.add(pedido)
            db.commit()
            db.refresh(pedido)
            detalle = models.DetallePedido(pedido_id=pedido.id, autoparte_id=ap.id, cantidad=2, precio_unitario=decimal.Decimal("12.34"))
            db.add(detalle)
            db.commit()
        else:
            detalle = db.query(models.DetallePedido).filter(models.DetallePedido.pedido_id == pedido.id).first()
            if not detalle:
                detalle = models.DetallePedido(pedido_id=pedido.id, autoparte_id=ap.id, cantidad=2, precio_unitario=decimal.Decimal("12.34"))
                db.add(detalle)
                db.commit()

        return {
            "rol_id": rol.id,
            "categoria_id": cat.id,
            "autoparte_id": ap.id,
            "inventario_id": inv.id if inv is not None else None,
            "estado_pend_id": estado_pend.id,
            "estado_surtido_id": estado_surtido.id,
            "usuario_email": usuario.email,
            "pedido_id": pedido.id,
            "detalle_cantidad": detalle.cantidad,
        }
    finally:
        db.close()


def test_get_reportes_summary():
    objs = seed_data()
    usuario_email = objs["usuario_email"]
    r = client.get("/reportes/", auth=(usuario_email, "pwd"))
    assert r.status_code == 200
    data = r.json()
    assert "ingresos_totales" in data
    assert "reporte_ventas" in data


def test_generar_reporte_inventario_pdf():
    objs = seed_data()
    usuario_email = objs["usuario_email"]
    r = client.get("/reportes/generar/inventario", params={"formato": "pdf"}, auth=(usuario_email, "pwd"))
    assert r.status_code == 200
    assert "application/pdf" in r.headers.get("content-type", "")


def test_pedidos_list_and_update_status():
    objs = seed_data()
    pedido_id = objs["pedido_id"]
    autoparte_id = objs["autoparte_id"]
    detalle_cantidad = objs["detalle_cantidad"]
    db = SessionLocal()
    try:
        inv_before = db.query(models.Inventario).filter(models.Inventario.autoparte_id == autoparte_id).first()
        assert inv_before is not None
        old_stock = inv_before.stock_actual
    finally:
        db.close()

    usuario_email = objs["usuario_email"]
    r = client.get("/pedidos/", auth=(usuario_email, "pwd"))
    assert r.status_code == 200
    lista = r.json()
    assert any(item.get("id") == pedido.id for item in lista)

    r = client.put(f"/pedidos/{pedido_id}/estatus", json={"estatus": "SURTIDO"}, auth=(usuario_email, "pwd"))
    assert r.status_code == 200
    assert r.json().get("estatus") == "SURTIDO"

    db = SessionLocal()
    try:
        inv_after = db.query(models.Inventario).filter(models.Inventario.autoparte_id == autoparte_id).first()
        assert inv_after.stock_actual == old_stock - detalle_cantidad
    finally:
        db.close()
