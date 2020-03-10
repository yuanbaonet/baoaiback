import os
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import config
from celery import Celery
import logging_config

db = SQLAlchemy()
Config = config[os.getenv('FLASK_CONFIG') or 'default']
celery = None

def create_app():
    app = Flask(__name__, static_url_path=Config.APP_STATIC_URL_PATH, static_folder=Config.STATIC_FOLDER)
    app.config.from_object(Config)
    db.init_app(app)
    db.app = app

    # 解决禁止跨域请求的问题
    if app.config['CORS_ENABLED']:
        CORS(app, supports_credentials=True)

    # init Celery # 初始化Celery
    # global celery
    # celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
    # celery.conf.update(app.config)

    # init modules # 初始化模块，将模块对应的命名空间增加到蓝图
    from . import modules
    modules.init_app(app)

    # register blueprint # 注册蓝图到应用
    from . import api
    api.init_api(app)

    return app # , celery
