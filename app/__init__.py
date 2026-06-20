from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    #Aqui importo los modelos aquí para que sean registrados por SQLAlchemy
    with app.app_context():
        from . import models  # Esto registra las clases de models.py
        db.create_all()       # Esto crea el archivo inventario.db automáticamente
 
    return app