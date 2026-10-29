import os
from pathlib import Path
from dotenv import load_dotenv

basedir = Path(__file__).resolve().parent.parent
load_dotenv(basedir / ".env")

class Config:
    #security
    SECRET_KEY = os.getenv("SECRET_KEY","secret_key_for_development_only_change_me")

    #database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{basedir / 'instance' / 'apartmentcare.db'}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #jwt
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt_secret_key_for_development_only_change_me")
