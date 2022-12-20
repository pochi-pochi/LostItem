from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from apps.app import db, login_manager


# db.Modelを継承したUserクラスの定義
class User(db.Model, UserMixin):
    __tablename__ = "users"
    # カラムの定義
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # passwordセットのためのプロパティ
    @property
    def password(self, password):
        raise AttributeError("読み取り不可")

    # passwordをハッシュ化してセット
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # password_check
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # ユーザ名の重複チェック
    def is_duplicate_username(self):
        return User.query.filter_by(username=self.username).first() is not None


# ログインしているユーザ情報を取得
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
