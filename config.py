import pymysql

pymysql.install_as_MySQLdb()

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

SECRET_KEY = 'tu_clave_secreta_aqui'
