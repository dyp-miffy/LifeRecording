from db import db

from models.diary import Diary

# 模型类
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(48), unique=True, nullable=False)
    password = db.Column(db.String(48))
    # 0代表普通用户，1代表管理员
    status = db.Column(db.Integer)
    # 一个用户有多个日记，diaries就是用户的集合对象（一对多）
    diaries = db.relationship("Diary", backref = "user")