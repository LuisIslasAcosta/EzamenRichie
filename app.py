from flask import Flask
from config import db, migrate
from dotenv import load_dotenv
import os
from flask import Blueprint
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger  # Importamos Flasgger

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Configuración de CORS
CORS(app, resources={r"/*": {"origins": "https://main.d3gd2kcl7rhrjn.amplifyapp.com"}})

# Configuración de JWT
app.config['JWT_SECRET_KEY'] = 'Prueba dia 08-02-2025'

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy, Flask-Migrate y JWTManager
db.init_app(app)
migrate.init_app(app, db)
jwt = JWTManager(app)

# Inicializar Swagger
swagger = Swagger(app)

# Ruta de prueba
@app.route('/')
def home():
    """
    Esta es la ruta de inicio de la API.
    ---
    responses:
      200:
        description: Bienvenida a la API.
    """
    return '¡Hola, esta es un API realizada para el proyecto de 5to cuatrimestre basada en un bastón inteligente'

# Importar los Blueprints de usuarios y roles
from routes.rutas import usuario_bp, roles_bp, baston_bp, ubicacion_bp

# Registrar los Blueprints
app.register_blueprint(usuario_bp, url_prefix='/usuario')
app.register_blueprint(roles_bp, url_prefix='/roles')
app.register_blueprint(baston_bp, url_prefix='/bastones')
app.register_blueprint(ubicacion_bp, url_prefix='/ubicaciones')

# Correr la aplicación
if __name__ == '__main__':
    app.run(debug=True)
