from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, length


# ユーザ新規登録とユーザ編集フォーム
class UserForm(FlaskForm):
    username = StringField(
        "ユーザ名",
        validators=[
            DataRequired(message="ユーザ名は必須です。"),
            length(max=30, message="30文字以内で入力してください。"),
        ],
    )

    password = PasswordField(
        "パスワード",
        validators=[
            DataRequired(message="パスワードは必須です。"),
        ],
    )

    submit = SubmitField("新規登録")
