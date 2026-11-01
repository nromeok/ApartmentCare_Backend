from flask import Flask
from app.extensions import db, migrate, jwt, cors
from app.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})

    # Import models
    from app import models  # noqa: F401

    # Import and register blueprints
    from app.routes.auth import auth_bp
    from app.routes.issues import issues_bp
    from app.routes.announcements import announcements_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(issues_bp, url_prefix="/api/issues")
    app.register_blueprint(announcements_bp, url_prefix="/api/announcements")

    return app