from datetime import datetime

from apps.app import db


class Items(db.Model):
    __tablename__ = "lostitems"
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String)
    item_color = db.Column(db.String)
    item_feature = db.Column(db.String)
    item_image_path = db.Column(db.String)
    item_floor = db.Column(db.String)
    item_place = db.Column(db.String)
    item_date = db.Column(db.DateTime, default=datetime.now)
    item_right = db.Column(db.Boolean, default=False)
    item_police = db.Column(db.DateTime, default=datetime.now)
