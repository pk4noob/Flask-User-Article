import os
from settings.settings import BasteSettings
from flask_sqlalchemy import SQLAlchemy

class ProdSettings(BasteSettings):
    DEBUG = False
    SQLALCHEMY_ECHO = False

    DB_NAME = os.getenv("DB_NAME", "postgres")
    DB_PORT = os.getenv("DB_PORT", 5432)
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_USER = os.getenv("DB_USER", "postgres")

    SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
