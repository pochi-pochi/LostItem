from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


class Search(FlaskForm):
    item_name = SelectField(
        label=("品目名"),
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

    submit = SubmitField("検索")


class DeleteItem(FlaskForm):
    submit = SubmitField("削除")
