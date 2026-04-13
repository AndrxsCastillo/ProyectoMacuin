import os
import json
import shutil
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


# Ensure the app uses a local sqlite file for tests before importing
os.environ["DATABASE_URL"] = "sqlite:///./test_api.db"

from app.main import app
from app.data.database import Base, engine, SessionLocal
from app import models
from app.crud.usuario import get_password_hash


def setup_module(module):
    # Create DB file and tables
    Base.metadata.create_all(bind=engine)


def teardown_module(module):
    # Remove the sqlite file produced during tests
    try:
        # Ensure the SQLAlchemy engine is closed before deleting the file
        try:
            from app.data.database import engine as _engine
            _engine.dispose()
        except Exception:
            pass
        # Leave DB file in place to avoid interfering with other test modules
        pass
    except FileNotFoundError:
        pass


def _create_initial_data():
    db: Session = SessionLocal()
    try:
        # Reuse if already exists (helps multiple test runs)
        rol = db.query(models.Rol).filter(models.Rol.nombre == "admin").first()
        if not rol:
            rol = models.Rol(nombre="admin", descripcion="Admin")
            db.add(rol)
            db.commit()
            db.refresh(rol)

        usuario = db.query(models.Usuario).filter(models.Usuario.email == "test@example.com").first()
        if not usuario:
            usuario = models.Usuario(nombre="Tester", email="test@example.com", password_hash=get_password_hash("pwd"), rol_id=rol.id)
            db.add(usuario)
            db.commit()
            db.refresh(usuario)
        else:
            # Ensure password is the expected test password
            usuario.password_hash = get_password_hash("pwd")
            db.add(usuario)
            db.commit()
            db.refresh(usuario)

        return rol, usuario
    finally:
        db.close()


def test_auth_and_roles():
    rol, usuario = _create_initial_data()
    client = TestClient(app)

    # Root endpoint from auth router
    r = client.get("/", auth=(usuario.email, "pwd"))
    assert r.status_code == 200
    assert "mensaje" in r.json()

    # Token endpoint (only checks existence of email)
    r = client.post("/token", data={"username": usuario.email, "password": "whatever"}, auth=(usuario.email, "pwd"))
    assert r.status_code == 200
    data = r.json()
    assert data.get("access_token") == usuario.email

    # Roles endpoint
    r = client.get("/roles/", auth=(usuario.email, "pwd"))
    assert r.status_code == 200
    roles = r.json()
    assert any(r.get("nombre") == "admin" for r in roles)


def test_usuarios_and_autopartes_endpoints():
    # Prepare: ensure admin user and create a category
    rol, usuario = _create_initial_data()
    db = SessionLocal()
    try:
        cat = db.query(models.Categoria).filter(models.Categoria.nombre == "Motores").first()
        if not cat:
            cat = models.Categoria(nombre="Motores", descripcion="Cat Motores")
            db.add(cat)
            db.commit()
            db.refresh(cat)
    finally:
        db.close()

    client = TestClient(app)

    # Create a user via API
    payload = {
        "nombre": "API User",
        "email": "apiuser@example.com",
        "password": "pwd",
        "rol_id": 1,
        "activo": True
    }
    r = client.post("/usuarios/", json=payload, auth=(usuario.email, "pwd"))
    assert r.status_code == 200
    user_json = r.json()
    assert user_json.get("email") == "apiuser@example.com"

    # Create an autoparte via API
    apayload = {
        "nombre": "FiltroAPI",
        "descripcion": "desc",
        "categoria_id": cat.id,
        "marca": "MarcaAPI",
        "precio": "15.50",
        "activo": True,
        "stock_inicial": 7,
        "stock_minimo": 1
    }
    r = client.post("/autopartes/", json=apayload, auth=(usuario.email, "pwd"))
    assert r.status_code == 200
    ap_json = r.json()
    assert ap_json.get("nombre") == "FiltroAPI"

    # List autopartes
    r = client.get("/autopartes/")
    assert r.status_code == 200
    lista = r.json()
    assert any(p.get("nombre") == "FiltroAPI" for p in lista)
