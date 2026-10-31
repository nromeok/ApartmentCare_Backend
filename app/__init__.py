from flask import Flask
from app.extensions import db, migrate
from app.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models so Flask-Migrate can detect them
    from app import models  

    #Import and register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(issues_bp, url_prefix="/issues")
    app.register_blueprint(announcements_bp, url_prefix="/announcements")

    return app