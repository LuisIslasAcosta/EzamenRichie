from flask import Blueprint, jsonify, request
from controllers.controllers import (
    create_usuario, get_usuario_por_id, edit_usuario, login_usuario
)
from models.models import Usuario

# Blueprints
usuario_bp = Blueprint('usuarios', __name__)

# -------------------------------------- Usuarios y Registros --------------------------- #

# Crear un nuevo usuario
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

    if not all([email, nombre, password, telefono]):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    return create_usuario(nombre, email, telefono, password)

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
                nombre:
                  type: string
                email:
                  type: string
                fecha_registro:
                  type: string
      401:
        description: Credenciales inválidas.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email y contraseña son requeridos"}), 400

    return login_usuario(email, password)

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
              nombre:
                type: string
              email:
                type: string
              password:
                type: string
              fecha_registro:
                type: string
    """
    try:
        usuarios = Usuario.query.all()
        return jsonify([usuario.to_dict() for usuario in usuarios]), 200
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": "Error al obtener los usuarios"}), 500

# Ruta para obtener un usuario por ID
@usuario_bp.route('/<int:usuario_id>', methods=['GET'])
def get_usuario(usuario_id):
    """
    Obtener un usuario por ID.
    --- 
    parameters:
      - name: usuario_id
        in: path
        type: integer
        required: true
        description: El ID del usuario.
    responses:
      200:
        description: Detalles del usuario.
        schema:
          type: object
          properties:
            nombre:
              type: string
            email:
              type: string
            password:
              type: string
            fecha_registro:
              type: string
      404:
        description: Usuario no encontrado.
    """
    return get_usuario_por_id(usuario_id)

# Ruta para editar un usuario
@usuario_bp.route('/<int:usuario_id>', methods=['PUT'])
def edit_usuario_route(usuario_id):
    """
    Editar un usuario.
    --- 
    parameters:
      - name: usuario_id
        in: path
        type: integer
        required: true
        description: El ID del usuario.
      - name: nombre
        in: body
        type: string
        description: El nombre del usuario.
      - name: email
        in: body
        type: string
        description: El correo electrónico del usuario.
      - name: password
        in: body
        type: string
        description: La contraseña del usuario.
      - name: telefono
        in: body
        type: string
        description: El teléfono del usuario.
    responses:
      200:
        description: Usuario actualizado exitosamente.
      404:
        description: Usuario no encontrado.
    """
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    telefono = data.get('telefono')
    password = data.get('password')

    return edit_usuario(usuario_id, nombre, email, telefono, password)

# Ruta para eliminar un usuario
@usuario_bp.route('/<int:usuario_id>', methods=['DELETE'])
def delete_usuario_route(usuario_id):
    """
    Eliminar un usuario.
    --- 
    parameters:
      - name: usuario_id
        in: path
        type: integer
        required: true
        description: El ID del usuario.
    responses:
      200:
        description: Usuario eliminado exitosamente.
      404:
        description: Usuario no encontrado.
    """
    try:
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({'msg': 'Usuario no encontrado'}), 404
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'msg': 'Usuario eliminado'}), 200
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({'msg': 'Error al eliminar el usuario'}), 500
