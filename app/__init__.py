import os
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    # Project root is the parent directory of the `app` package
    project_root = Path(__file__).resolve().parent.parent
    templates_path = project_root / 'templates'

    # Fallbacks: if templates not found at project root, try app/templates
    if not templates_path.exists():
        alt = Path(__file__).resolve().parent / 'templates'
        if alt.exists():
            templates_path = alt

    app = Flask(__name__, template_folder=str(templates_path))
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        from . import models  # Esto registra las clases de models.py

        # Ensure tables exist for current models
        db.create_all()

    return app