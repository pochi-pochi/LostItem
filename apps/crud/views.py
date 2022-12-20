from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required

from apps.app import db
from apps.crud.forms import UserForm
from apps.crud.models import User

# Blueprintでcrudアプリの生成
crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)


# indexエンドポイントの作成
@crud.route("/")
def index():
    return render_template("crud/index.html")


# ユーザの新規登録、編集
@crud.route("/users/new", methods=["GET", "POST"])
def create_user():
    form = UserForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            password=form.password.data,
        )

        # ユーザを追加
        db.session.add(user)
        db.session.commit()

        # ユーザの一覧画面へリダイレクト
        return redirect(url_for("crud.users"))
    return render_template("crud/create.html", form=form)


# ユーザ一覧の取得
@crud.route("/users")
@login_required
def users():
    users = User.query.all()
    return render_template("crud/index.html", users=users)


# ユーザの編集画面
@crud.route("/users/<user_id>", methods=["POST", "GET"])
@login_required
def edit_user(user_id):
    form = UserForm()
    user = User.query.filter_by(id=user_id).first()

    # サブミットの場合、ユーザ情報を更新
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))

    # GETの場合はhtmlを返す
    return render_template("crud/edit.html", user=user, form=form)


# ユーザ削除
@crud.route("/user/<user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("crud.users"))
