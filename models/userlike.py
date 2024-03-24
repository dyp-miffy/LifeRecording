from db import db

# 模型类
from models import user, diary


class Userlike(db.Model):
    __tablename__ ="userlike"
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer)
    diary_id = db.Column(db.Integer)
    is_like = db.Column(db.Integer)#0代表不喜欢，1代表赞
    # db.ForeignKey='user.id,diary.id'
