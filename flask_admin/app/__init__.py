from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    
    # Llave secreta para manejar las sesiones de los usuarios (login)
    app.config['SECRET_KEY'] = 'macuin_super_secreto_2026'
    
    # URL de nuestra API Central (FastAPI)
    # Usaremos localhost por ahora, pero en Docker apuntará al contenedor
    app.config['API_URL'] = os.environ.get('API_URL', 'http://flask_admin:8000')

    # Registramos las rutas
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app