from flask_env import MetaFlaskEnv
import os


class BasteSettings(metaclass=MetaFlaskEnv):
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False