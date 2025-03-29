from config import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from decimal import Decimal

# Modelo de Usuario
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'email': self.email,
            'password': self.password,
            'fecha_registro': self.fecha_registro
        }

    def set_password(self, password):
        """Genera el hash de la contraseña"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verifica la contraseña utilizando el hash almacenado"""
        return check_password_hash(self.password, password)
