from sqlalchemy import text
from app.data.database import engine

def probar_conexion():
    try:
        # Intentamos conectarnos y hacer una consulta simple
        with engine.connect() as conexion:
            resultado = conexion.execute(text("SELECT 1"))
            print("✅ ¡Conexión exitosa, bro! La contraseña y el usuario son correctos.")
    except Exception as e:
        print("❌ Error al conectar. Revisa tus credenciales.")
        print(f"Detalle del error: {e}")

if __name__ == "__main__":
    probar_conexion()