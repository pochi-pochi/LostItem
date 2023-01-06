from flask_wtf.form import FlaskForm
from wtforms.fields import (
    BooleanField,
    DateField,
    SelectField,
    SubmitField,
    TextAreaField,
)


class RegisterItemForm(FlaskForm):
    item_name = SelectField(
        label=("品目"),
        choices=[
            ("ボールペン", "ボールペン"),
            ("バナナ", "バナナ"),
            ("コーヒーマグ", "コーヒーマグ"),
            ("その他", "その他"),
        ],
    )

    item_color = SelectField(
        label=("色"),
        choices=[
            ("赤系", "赤系"),
            ("青系", "青系"),
            ("緑系", "緑系"),
            ("柄", "柄"),
            ("その他", "その他"),
        ],
    )

    item_feature = TextAreaField("特徴")

    item_floor = SelectField(
        label=("拾得場所"),
        choices=[
            ("1階", "1階"),
            ("2階", "2階"),
            ("3階", "3階"),
            ("4階", "4階"),
        ],
    )

    item_place = SelectField(
        label=("保管場所"),
        choices=[
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
            ("D", "D"),
        ],
    )

    item_right = BooleanField("権利主張")

    item_police = DateField("警察届け予定日")

    submit = SubmitField("登録")
