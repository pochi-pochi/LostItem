from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    send_from_directory,
    url_for,
)

from apps.app import db
from apps.detector.forms import RegisterItemForm
from apps.detector.models import Items
from apps.search_items.forms import DeleteItem, Search

# アプリのインスタンス生成
search_items = Blueprint(
    "search_items", __name__, template_folder="templates", static_folder="static"
)


# indexエンドポイント
@search_items.route("/", methods=["GET", "POST"])
def index():
    search_form = Search()
    if search_form.validate_on_submit():
        items_name = search_form.item_name.data
        items_color = search_form.item_color.data
        return redirect(
            url_for("search_items.tables", item_name=items_name, item_color=items_color)
        )

    return render_template("search_items/index.html", search_form=search_form)


# 検索結果の一覧表示
@search_items.route("/tables/<item_name>/<item_color>")
def tables(item_name, item_color):
    search_images = (
        db.session.query(Items)
        .filter_by(item_name=item_name, item_color=item_color)
        .all()
    )

    return render_template("search_items/tables.html", search_images=search_images)


# 指定したアイテムの編集画面
@search_items.route("/edit_items/<itemid>", methods=["GET", "POST"])
def edit_items(itemid):
    form = RegisterItemForm()
    deleteform = DeleteItem()

    # idより拾得物取得
    item = Items.query.filter_by(item_id=itemid).first()

    # formからsubmitされた場合は情報を更新し、拾得物一覧画面へ
    if form.validate_on_submit():
        item.item_name = form.item_name.data
        item.item_color = form.item_color.data
        item.item_feature = form.item_feature.data
        db.session.add(item)
        db.session.commit()
        return redirect(url_for("search_items.all"))

    if deleteform.validate_on_submit():
        redirect(url_for("search_items.delete_item"))

    return render_template(
        "search_items/edit_items.html", item=item, form=form, deleteform=deleteform
    )


# 指定したアイテムの削除
@search_items.route("/delete/<item_id>", methods=["GET", "POST"])
def delete_item(item_id):
    item = Items.query.filter_by(item_id=item_id).first()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("search_items.edit_items"))


# 画像の表示
@search_items.route("/images/<path:filename>")
def image_file(filename):
    filename = filename[53:]
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)
