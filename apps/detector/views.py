import json
import os
import shutil
import uuid
from pathlib import Path

import numpy as np
import torch
from flask import Blueprint, current_app, render_template
from flask_login import login_required
from PIL import Image
from torchvision import transforms

from apps.app import db
from apps.detector.forms import RegisterItemForm
from apps.detector.models import Items

dt = Blueprint(
    "detector",
    __name__,
    template_folder="templates",
)


# 拾得物管理アプリのトップぺージ
@dt.route("/")
def index():
    return render_template("detector/index.html")


# 拾得物撮影画面
@dt.route("/register")
@login_required
def register():
    # 本来ならここに削除のスクリプトを書きたかったが、
    # 難しそうなのでファイルの保存期間から削除
    return render_template("detector/register.html")


# 拾得物検索画面
@dt.route("/search")
@login_required
def search():
    return render_template("detector/search.html")


# 拾得物登録画面
@dt.route("/display_image", methods=["GET", "POST"])
@login_required
def display_image():

    # フォームからの情報をデータベースへ格納
    register_form = RegisterItemForm()
    if not register_form.validate_on_submit():
        # 画像の解析
        net = torch.load(Path(current_app.root_path, "detector", "vgg16.pt"))
        net = net.eval()
        resize = 224
        mean = (0.485, 0.456, 0.406)
        std = (0.229, 0.224, 0.225)
        ILSVRC_class_index = json.load(
            open(
                Path(current_app.root_path, "detector", "imagenet_class_index.json"),
                "r",
            )
        )
        # ILSVRCPredictorのインスタンスを生成します
        predictor = ILSVRCPredictor(ILSVRC_class_index)

        # 入力画像を読み込む
        image_file_path = Path(
            current_app.root_path, "detector", "images", "captured-video.jpg"
        )
        img = Image.open(image_file_path).convert(
            "RGB"
        )  # [高さ][幅][色RGB] ついでにチャンネル数を3にしてる

        # 前処理の後、バッチサイズの次元を追加する
        transform = BaseTransform(resize, mean, std)  # 前処理クラス作成
        img_transformed = transform(img)  # torch.Size([3, 224, 224])
        inputs = img_transformed.unsqueeze_(0)  # torch.Size([1, 3, 224, 224])

        # モデルに入力し、モデル出力をラベルに変換する
        out = net(inputs)  # torch.Size([1, 1000])
        result = predictor.predict_max(out)

        if result == "coffe_mug":
            result = "コーヒーマグ"
        elif result == "ballpoint":
            result = "ボールペン"
        elif result == "banana":
            result = "バナナ"
        else:
            result = "その他"

        picture_name = Path(
            current_app.root_path, "detector", "images", "captured-video.jpg"
        )

    else:
        # 画像取得元
        source_folder = Path(current_app.root_path, "detector", "images")
        # 画像移動先フォルダ
        destination_folder = Path(current_app.root_path, "detector", "renamed_images")

        # ファイル名と拡張子を取得、ファイル名をuuidに
        originnl_filename = "captured-video.jpg"
        new_filename = str(uuid.uuid4())
        _, file_extention = os.path.splitext(originnl_filename)
        new_filename = new_filename + file_extention
        originnl_filename = os.path.join(source_folder, originnl_filename)
        new_filename = os.path.join(source_folder, new_filename)
        os.rename(originnl_filename, new_filename)

        # 画像の移動
        for file in os.listdir(source_folder):
            file_path = os.path.join(source_folder, new_filename)
            moved_path = shutil.move(file_path, destination_folder)

        # imagesに登録されている写真の削除
        sourcefoder = Path(current_app.root_path, "detector", "images")
        for filename in os.listdir(sourcefoder):
            file_path = os.path.join(sourcefoder, filename)
            os.unlink(file_path)

        # データベースへ格納
        new_item = Items(
            item_name=register_form.item_name.data,
            item_color=register_form.item_color.data,
            item_feature=register_form.item_feature.data,
            item_image_path=moved_path,
        )
        db.session.add(new_item)
        db.session.commit()

        return render_template("detector/commit.html")

    return render_template(
        "detector/display_image.html",
        picture_name=picture_name,
        result=result,
        register_form=register_form,
    )


# 入力画像の前処理のクラス
class BaseTransform:
    def __init__(self, resize, mean, std):
        self.base_transform = transforms.Compose(
            [
                transforms.Resize(resize),  # 短い辺の長さがresizeの大きさになる
                transforms.CenterCrop(resize),  # 画像中央をresize × resizeで切り取り
                transforms.ToTensor(),  # Torchテンソルに変換
                transforms.Normalize(mean, std),  # 色情報の標準化
            ]
        )

    def __call__(self, img):
        return self.base_transform(img)


# 出力結果からラベルを予測する後処理クラス
class ILSVRCPredictor:
    def __init__(self, class_index):
        self.class_index = class_index

    def predict_max(self, out):
        maxid = np.argmax(out.detach().numpy())
        predicted_label_name = self.class_index[str(maxid)][1]

        return predicted_label_name


@dt.route("/commit", methods=["POST"])
def commit():
    return render_template("detector/commit.html")
