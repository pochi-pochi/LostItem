from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, SubmitField


class Search(FlaskForm):
    item_name = SelectField(
        label=("品目名"),
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

    submit = SubmitField("検索")


class DeleteItem(FlaskForm):
    submit = SubmitField("削除")


class Police(FlaskForm):
    item_police = DateField("警察届出予定日")
    submit = SubmitField("検索")
