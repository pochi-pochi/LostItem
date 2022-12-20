from flask_wtf.form import FlaskForm
from wtforms.fields import SelectField, SubmitField, TextAreaField


class RegisterItemForm(FlaskForm):
    item_name = SelectField(
        label=("品目"),
        choices=[
            ("ballpoint", "ボールペン"),
            ("banana", "バナナ"),
            ("coffee_mug", "コーヒーマグ"),
            ("other", "その他"),
        ],
    )

    item_color = SelectField(
        label=("色"),
        choices=[
            ("red", "赤系"),
            ("blue", "青系"),
            ("green", "緑系"),
            ("patterned", "柄"),
            ("other", "その他"),
        ],
    )

    item_feature = TextAreaField("特徴")

    submit = SubmitField("登録")
