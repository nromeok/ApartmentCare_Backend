from flask import Flask
from app.extensions import db, migrate,jwt,cors
from app.config import Config



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models so Flask-Migrate can detect them
    from app import models  
    from app.routes.auth import auth_bp
    from app.routes.issues import issues_bp
    from app.routes.announcements import announcements_bp

    #Import and register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(issues_bp, url_prefix="/issues")
    app.register_blueprint(announcements_bp, url_prefix="/announcements")

    return app