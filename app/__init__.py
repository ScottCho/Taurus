import os

from flask import Flask, render_template
from app.extensions import db, migrate, scheduler

from app.blueprints.goods import goods_bp


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def index():
        return render_template('index.html')

    register_extensions(app)
    register_blueprints(app)
    return app


# 注册拓展
def register_extensions(app):
    db.init_app(app)
    db.app = app
    migrate.init_app(app, db)
    scheduler.init_app(app)
    scheduler.start()


# 注册蓝图
def register_blueprints(app):
    app.register_blueprint(goods_bp)
