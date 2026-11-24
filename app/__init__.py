from flask import Flask
from config import Config
from .extensions import db, migrate

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models  # make sure models are registered for migrations

    from .routes.main import bp as main_bp
    from .routes.users import bp as users_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp)

    return app