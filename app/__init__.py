from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    # __name__ 决定应用根目录
    app = Flask(__name__)
    # 初始化app配置
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 扩展应用初始化
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    #初始化蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .fiction import fiction as fiction_blueprint
    app.register_blueprint(fiction_blueprint)

    return app
