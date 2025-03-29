from models.models import Usuario
from flask import jsonify
from config import db
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

# Obtener un usuario por su ID
def get_usuario_por_id(usuario_id):
    try:
        # Buscar el usuario por su ID
        usuario = Usuario.query.get(usuario_id)
        
        # Si el usuario no existe, devolver un mensaje de error
        if not usuario:
            return jsonify({'msg': 'Usuario no encontrado'}), 404
        
        # Devolver los datos del usuario encontrado (solo lo necesario)
        return jsonify(usuario.to_dict()), 200
        
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al obtener el usuario'}), 500

# Editar un usuario
def edit_usuario(usuario_id, nombre=None, email=None, telefono=None, password=None):
    try:
        # Buscar el usuario por su ID
        usuario = Usuario.query.get(usuario_id)
        
        # Si el usuario no existe, devolver un mensaje de error
        if not usuario:
            return jsonify({'msg': 'Usuario no encontrado'}), 404
        
        # Actualizar los campos solo si se proporcionan nuevos valores
        if nombre:
            usuario.nombre = nombre
        if email:
            usuario.email = email
        if telefono:
            usuario.telefono = telefono
        if password:
            usuario.password = password
        
        # Guardar los cambios en la base de datos
        db.session.commit()
        
        # Devolver el usuario actualizado (solo lo necesario)
        return jsonify(usuario.to_dict()), 200
        
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al editar el usuario'}), 500

# Crear un nuevo usuario
def create_usuario(nombre, email, telefono, password):
    try:
        nuevo_usuario = Usuario(nombre=nombre, email=email, telefono=telefono)
        nuevo_usuario.set_password(password)  # Establecer la contraseña cifrada
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify(nuevo_usuario.to_dict()), 201
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al crear el usuario'}), 500

# Iniciar sesión de un usuario
def login_usuario(email, password):
    try:
        # Buscar el usuario por su email
        usuario = Usuario.query.filter_by(email=email).first()

        # Verificar si el usuario existe y si la contraseña es correcta
        if usuario and usuario.check_password(password):  # Verificación de la contraseña
            # Si las credenciales son correctas, devolver solo los datos del usuario sin token
            return jsonify({
                'usuario': {
                    'nombre': usuario.nombre,
                    'email': usuario.email,
                    'fecha_registro': usuario.fecha_registro
                }
            }), 200
        else:
            # Si las credenciales son incorrectas
            return jsonify({"msg": "Credenciales inválidas"}), 401
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error en el login'}), 500
