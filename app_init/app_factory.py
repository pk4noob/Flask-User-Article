from flask import Flask
import os
import logging
import sys
from logging.config import dictConfig
from extensions.extensions import ma, db,jwt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging

settings = {
    "dev": "settings.devsettings.DevelopSettings",
    "prod": "settings.prodsettings.ProdSettings"
}


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s.%(msecs)03d] %(levelname)s %(name)s:%(funcName)s:%(message)s  %(module)s: %(message)s',
    }},

       'handlers': 
    {
        'wsgi':{
        'class' : 'logging.FileHandler',
        'formatter': 'default',
        'filename' : 'WARN.log'
        },
        'custom_handler': {
        'class' : 'logging.FileHandler',
        'formatter': 'default',
        'filename' : 'WARN.log'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    },
    'MyExample': {
        'level': 'WARN',
        'handlers' : 'custom_handler'
    }
})

# dictConfig(
#             {
#     'version': 1,
#     'formatters': {
#             'default': {
#                         'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
#                        },
#             'simpleformatter' : {
#                         'format' : '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#             }
#     },
#     'handlers': 
#     {
#         'wsgi': {
#         'class': 'logging.StreamHandler',
#         'formatter': 'default'
#                 },
#         'custom_handler': {
#         'class' : 'logging.FileHandler',
#         'formatter': 'simpleformatter',
#         'filename' : 'WARN.log'
#         }
#     },
#     'root': {
#         'level': 'INFO',
#         'handlers': ['wsgi']
#     },
#     'MyExample': {
#         'level': 'WARN',
#         'handlers' : 'custom_handler'
#     }
# })

def get_settings(settings_name):
    if settings.get(settings_name):
        return settings.get(settings_name)
    raise Exception("Gosterdiyin %s parametr yanlisdir :" % settings_name)


def createAp(settings_name):
    app = Flask(__name__)
    Logger = logging.getLogger(__name__)
    handler = logging.StreamHandler(sys.stdout)
    settings_obg = get_settings(settings_name)
    app.config.from_object(settings_obg)
    app.logger.addHandler(handler)
    migrate = Migrate(app, db)
    jwt.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    ctx = app.app_context()
    ctx.push()
    return app