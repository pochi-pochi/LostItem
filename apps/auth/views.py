from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user

from apps.app import db
from apps.auth.forms import LoginForm, SignUpForm
from apps.crud.models import User

auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
)


# サインアップ用のルート
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            password=form.password.data,
        )

        # ユーザ名の重複チェック
        if user.is_duplicate_username():
            flash("そのユーザ名はすでに使われています。")
            return redirect(url_for("auth.signup"))

        db.session.add(user)
        db.session.commit()

        # ユーザ情報をセッションに格納
        login_user(user)

        # GETパラメータにnextが存在し、値が名いい場合はユーザ一覧へ
        next_ = request.args.get("next")
        if next_ is None or not next_.startswith("/"):
            next_ = url_for("detector.index")
        return redirect(next_)

    return render_template("auth/signup.html", form=form)


# ログイン用のルート
@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # ユーザの存在を確認後、パスワードが一致すれば許可
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for("detector.index"))

        flash("ユーザーネームが存在しないかパスワードが間違っています。")
    return render_template("auth/login.html", form=form)


# ログアウト用
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
