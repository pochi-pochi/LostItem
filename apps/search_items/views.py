from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    send_from_directory,
    url_for,
)
from flask_login import login_required

from apps.app import db
from apps.detector.forms import RegisterItemForm
from apps.detector.models import Items
from apps.search_items.forms import All, DeleteItem, Police, Search

# アプリのインスタンス生成
search_items = Blueprint(
    "search_items", __name__, template_folder="templates", static_folder="static"
)


# indexエンドポイント
@search_items.route("/", methods=["GET", "POST"])
@login_required
def index():
    search_form = Search()
    if search_form.validate_on_submit():
        items_name = search_form.item_name.data
        items_color = search_form.item_color.data
        return redirect(
            url_for("search_items.tables", item_name=items_name, item_color=items_color)
        )

    all_form = All()
    if all_form.validate_on_submit():
        all_items = db.session.query(Items).all()

        return render_template("search_items/all.html", all_items=all_items)

    return render_template(
        "search_items/index.html", search_form=search_form, all_form=all_form
    )


# 検索結果の一覧表示
@search_items.route("/tables/<item_name>/<item_color>")
@login_required
def tables(item_name, item_color):
    search_images = (
        db.session.query(Items)
        .filter_by(item_name=item_name, item_color=item_color)
        .all()
    )

    return render_template("search_items/tables.html", search_images=search_images)


# 指定したアイテムの編集画面
@search_items.route("/edit_items/<itemid>", methods=["GET", "POST"])
@login_required
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
        item.item_floor = form.item_floor.data
        item.item_place = form.item_place.data
        item.item_right = form.item_right.data
        item.item_police = form.item_police.data
        db.session.add(item)
        db.session.commit()
        return redirect(url_for("search_items.index"))

    if deleteform.validate_on_submit():
        redirect(url_for("search_items.delete_item", itemid=item.item_id))

    return render_template(
        "search_items/edit_items.html", item=item, form=form, deleteform=deleteform
    )


# 指定したアイテムの削除
@search_items.route("/delete/<itemid>", methods=["GET", "POST"])
@login_required
def delete_item(itemid):
    item = Items.query.filter_by(item_id=itemid).first()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("search_items.index"))


# 画像の表示
@search_items.route("/images/<path:filename>")
@login_required
def image_file(filename):
    filename = filename[53:]
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


# 警察届出物品の検索
@search_items.route("/police", methods=["GET", "POST"])
@login_required
def police():
    police_form = Police()

    if police_form.validate_on_submit():
        item_police = police_form.item_police.data
        return redirect(url_for("search_items.police_tables", item_police=item_police))

    return render_template("search_items/police.html", police_form=police_form)


# 警察届出物品の一覧
@search_items.route("/police_tables/<item_police>")
@login_required
def police_tables(item_police):
    item_police += " 00:00:00.000000"
    print(item_police)
    police_items = db.session.query(Items).filter_by(item_police=item_police).all()

    return render_template("search_items/police_tables.html", police_items=police_items)
