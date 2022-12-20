from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from apps.config import config

db = SQLAlchemy()

csrf = CSRFProtect()

# LoginManagerのインスタンス化
login_manager = LoginManager()
# # login_view属性に未ログイン時にリダイレクトするエンドポイントを指定
# login_manager.login_view = "auth.signup"
# # login_message属性にログイン後に表示するメッセージを指定（ここでは空欄）
# login_manager.login_message = ""


def create_app(config_key):
    app = Flask(__name__)

    # コンフィグ設定
    app.config.from_object(config[config_key])

    csrf.init_app(app)

    db.init_app(app)
    # Migrateとappの連携
    Migrate(app, db)

    login_manager.init_app(app)

    # crudアプリの登録
    from apps.crud import views as crud_views

    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    # authアプリの登録
    from apps.auth import views as auth_vews

    app.register_blueprint(auth_vews.auth, url_prefix="/auth")
    # detectorアプリの登録
    from apps.detector import views as dt_views

    app.register_blueprint(dt_views.dt, url_prefix="/")

    # searchアプリの登録
    from apps.search_items import views as search_views

    app.register_blueprint(search_views.search_items, url_prefix="/search_items")

    return app
