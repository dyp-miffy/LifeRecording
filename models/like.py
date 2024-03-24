from db import db

# 模型类
class Like(db.Model):
    __tablename__ = "like"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer)
    licount = db.Column(db.Integer)