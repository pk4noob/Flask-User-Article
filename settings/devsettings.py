from settings.settings import BasteSettings
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta


class DevelopSettings(BasteSettings):
    DEBUG = True
    JWT_SECRET_KEY = os.urandom(32)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=150)
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:test123@127.0.0.1:5432/userArticleDb"
    SQLALCHEMY_ECHO = False
    