from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.controllers import get_all_roles, create_rol, create_usuario, get_all_bastones, create_baston
from controllers.controllers import edit_usuario, get_usuario_por_id, delete_baston, create_access_token
from controllers.controllers import get_all_ubicaciones, create_ubicacion, asignar_baston_usuario
from models.models import Usuario

# Blueprints
usuario_bp = Blueprint('usuarios', __name__)
roles_bp = Blueprint('roles', __name__)
baston_bp = Blueprint('bastones', __name__)
ubicacion_bp = Blueprint('ubicaciones', __name__)

# ------------------------------------- Roles -------------------------------------- #

@roles_bp.route('/roles', methods=['GET'])
def obtener_roles():
    """
    Obtiene todos los roles.
    ---
    responses:
      200:
        description: Lista de roles disponibles.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              nombre:
                type: string
    """
    return get_all_roles()

@roles_bp.route('/', methods=['POST'])
def create_rol_route():
    """
    Crear un nuevo rol.
    ---
    parameters:
      - name: nombre
        in: body
        type: string
        required: true
        description: El nombre del rol.
    responses:
      200:
        description: Rol creado exitosamente.
      400:
        description: Faltan campos requeridos.
    """
    data = request.get_json()
    nombre = data.get('nombre')
    
    if not nombre:
        return jsonify({"error": "Faltan campos requeridos"}), 400
    
    return create_rol(nombre)

# -------------------------------------- Usuarios y Registros --------------------------- #

@usuario_bp.route('/', methods=['POST'])
def usuario_store():
    """
    Crear un nuevo usuario.
    ---
    parameters:
      - name: email
        in: body
        type: string
        required: true
        description: El correo electrónico del usuario.
      - name: nombre
        in: body
        type: string
        required: true
        description: El nombre del usuario.
      - name: password
        in: body
        type: string
        required: true
        description: La contraseña del usuario.
      - name: telefono
        in: body
        type: string
        required: true
        description: El teléfono del usuario.
    responses:
      200:
        description: Usuario creado exitosamente.
      400:
        description: Faltan campos requeridos.
    """
    data = request.get_json()
    email = data.get('email')
    nombre = data.get('nombre')
    password = data.get('password')
    telefono = data.get('telefono')

    rol_id = data.get('rol_id', 1)  # Asignar rol_id 1 por defecto (usuario regular)

    if not all([email, nombre, password, telefono]):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    return create_usuario(nombre, email, telefono, password, rol_id)

@usuario_bp.route('/login', methods=['POST'])
def login_usuario_route():
    """
    Login de usuario.
    ---
    parameters:
      - name: email
        in: body
        type: string
        required: true
        description: El correo electrónico del usuario.
      - name: password
        in: body
        type: string
        required: true
        description: La contraseña del usuario.
    responses:
      200:
        description: Login exitoso, se genera un token de acceso.
        schema:
          type: object
          properties:
            access_token:
              type: string
              description: El token de acceso JWT.
            usuario:
              type: object
              properties:
                id:
                  type: integer
                nombre:
                  type: string
                email:
                  type: string
                telefono:
                  type: string
                rol_id:
                  type: integer
                rol_nombre:
                  type: string
      401:
        description: Credenciales inválidas.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email y contraseña son requeridos"}), 400

    try:
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.check_password(password):
            access_token = create_access_token(identity=usuario.id)
            return jsonify({
                "message": "Login exitoso",
                "access_token": access_token,
                "usuario": {
                    "id": usuario.id,
                    "nombre": usuario.nombre,
                    "email": usuario.email,
                    "telefono": usuario.telefono,
                    "rol_id": usuario.rol_id,
                    "rol_nombre": usuario.rol.nombre
                }
            }), 200
        else:
            return jsonify({"error": "Credenciales inválidas"}), 401
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": "Login fallido"}), 500

# Ruta para obtener todos los usuarios
@usuario_bp.route('/obtener', methods=['GET'])
def get_usuarios():
    """
    Obtener todos los usuarios.
    ---
    responses:
      200:
        description: Lista de usuarios.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              nombre:
                type: string
              email:
                type: string
              telefono:
                type: string
              rol_id:
                type: integer
    """
    try:
        usuarios = Usuario.query.all()
        return jsonify([usuario.to_dict() for usuario in usuarios]), 200
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": "Error al obtener los usuarios"}), 500

# ---------------------------------------- Bastones -------------------------------- #

@baston_bp.route('/create_baston', methods=['POST'])
def create_baston_route():
    """
    Crear un nuevo bastón.
    ---
    parameters:
      - name: nombre
        in: body
        type: string
        required: true
        description: El nombre del bastón.
    responses:
      200:
        description: Bastón creado exitosamente.
      400:
        description: Faltan campos requeridos.
    """
    data = request.get_json()
    nombre = data.get('nombre')

    if not nombre:
        return jsonify({'msg': 'El nombre es obligatorio'}), 400

    return create_baston(nombre)

@baston_bp.route('/bastones', methods=['GET'])
def get_all_bastones_route():
    """
    Obtener todos los bastones.
    ---
    responses:
      200:
        description: Lista de bastones.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              nombre:
                type: string
    """
    return get_all_bastones()

# ----------------------------------- Ubicaciones ---------------------------------#

@ubicacion_bp.route('/ubicaciones', methods=['GET'])
def obtener_ubicaciones():
    """
    Obtener todas las ubicaciones.
    ---
    responses:
      200:
        description: Lista de ubicaciones.
        schema:
          type: array
          items:
            type: object
            properties:
              latitud:
                type: number
              longitud:
                type: number
              direccion:
                type: string
    """
    try:
        return get_all_ubicaciones()
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": "Error al obtener las ubicaciones"}), 500
