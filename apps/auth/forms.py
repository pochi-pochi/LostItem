from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


# サインアップフォーム
class SignUpForm(FlaskForm):
    username = StringField(
        "ユーザ名",
        validators=[
            DataRequired("ユーザ名は必須です。"),
            Length(1, 30, "30文字以内で入力してください。"),
        ],
    )

    password = PasswordField("パスワード", validators=[DataRequired("パスワードは必須です。")])
    submit = SubmitField("新規登録")


class LoginForm(FlaskForm):
    username = StringField(
        "ユーザ名",
        validators=[
            DataRequired("ユーザ名は必須です。"),
        ],
    )

    password = PasswordField("パスワード", validators=[DataRequired("パスワードは必須です。")])
    submit = SubmitField("ログイン")
