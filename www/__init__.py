import os
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import config
from celery import Celery
import arrow
import logging_config

db = SQLAlchemy()
Config = config[os.getenv('FLASK_CONFIG') or 'default']
celery = None

def create_app():
    app = Flask(__name__, static_url_path=Config.APP_STATIC_URL_PATH, static_folder=Config.STATIC_FOLDER, template_folder=Config.SITE_TEMPLATE_FOLDER)
    app.config.from_object(Config)
    db.init_app(app)
    db.app = app
    # 解决禁止跨域请求的问题
    if app.config['CORS_ENABLED']:
        CORS(app, supports_credentials=True)

    # init Celery
    # global celery
    # celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
    # celery.conf.update(app.config)

    from . import modules
    modules.init_app(app)

    @app.template_global('now')
    def now_datetime(format='YYYY-MM-DD HH:mm:ss'):
        return arrow.now().format(format)
    return app #, celery
