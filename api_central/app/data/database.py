from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Cambia "root:password" por tus credenciales de MySQL local. 
# Más adelante, para Docker, cambiaremos "localhost" por el nombre del contenedor de la BD.
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:123456@db:5432/autopartes_db"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia para inyectar la sesión de la BD en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
