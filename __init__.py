from flask import Flask
from flask_migrate import Migrate
from .config import Config
from .extensions import db
from .models import init_db
from .routes import init_routes
from flask_jwt_extended import JWTManager
from flask_cors import CORS

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)
    db.init_app(app)
    jwt = JWTManager(app)
    init_db(app)
    init_routes(app)
    migrate = Migrate(app, db)

    return app
    