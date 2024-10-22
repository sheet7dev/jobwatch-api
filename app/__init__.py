import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config

from .models import db

migrate = Migrate()
jwt = JWTManager()


def create_app(test_config=None):
    app = Flask(__name__)
    if test_config:
        app.config.from_object(test_config)
    else:
        app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app