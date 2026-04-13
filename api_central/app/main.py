from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.data.database import engine, Base, SessionLocal
import app.models
from app.routers import auth, usuarios, autopartes, categorias, pedidos, reportes, cliente
import bcrypt

try:
    Base.metadata.create_all(bind=engine)
    print("Conexión inicial a la BD exitosa.")
except Exception as e:
    print(f"BD no lista en el arranque. Omitiendo create_all. Error: {e}")


def seed_db():
    """Siembra datos iniciales: roles, 2 usuarios y estados de pedido."""
    db = SessionLocal()
    try:
        # ── Roles ───────────────────────────────────────────────────────────
        rol_admin = db.query(app.models.Rol).filter_by(nombre="Administrador").first()
        if not rol_admin:
            rol_admin = app.models.Rol(nombre="Administrador", descripcion="Administrador del sistema")
            db.add(rol_admin)
            db.flush()

        rol_cliente = db.query(app.models.Rol).filter_by(nombre="Usuario").first()
        if not rol_cliente:
            rol_cliente = app.models.Rol(nombre="Usuario", descripcion="Usuario cliente de la tienda")
            db.add(rol_cliente)
            db.flush()

        # ── Usuarios ────────────────────────────────────────────────────────
        if not db.query(app.models.Usuario).filter_by(email="admin@macuin.com").first():
            hashed = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode()
            db.add(app.models.Usuario(
                nombre="Administrador",
                email="admin@macuin.com",
                password_hash=hashed,
                rol_id=rol_admin.id,
                activo=True,
            ))

        if not db.query(app.models.Usuario).filter_by(email="usuario@macuin.com").first():
            hashed = bcrypt.hashpw(b"usuario123", bcrypt.gensalt()).decode()
            db.add(app.models.Usuario(
                nombre="Usuario",
                email="usuario@macuin.com",
                password_hash=hashed,
                rol_id=rol_cliente.id,
                activo=True,
            ))

        # ── Estados de pedido ────────────────────────────────────────────────
        for nombre in ["PENDIENTE", "Recibido", "Surtido", "Enviado"]:
            if not db.query(app.models.EstadoPedido).filter_by(nombre=nombre).first():
                db.add(app.models.EstadoPedido(nombre=nombre))

        db.commit()
        print("Seed completado: roles, usuarios y estados de pedido listos.")
    except Exception as e:
        db.rollback()
        print(f"Error en seed: {e}")
    finally:
        db.close()


try:
    seed_db()
except Exception as e:
    print(f"Seed omitido: {e}")

app = FastAPI(title="API Central - MACUIN") # SIN dependencias globales

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers SIN el candado verify_basic
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(autopartes.router)
app.include_router(categorias.router)
app.include_router(pedidos.router)
app.include_router(reportes.router)
app.include_router(cliente.router)