from db import db

# 模型类
class Diary(db.Model):
    __tablename__ ="diary"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DATE)
    text = db.Column(db.Text)
    mood = db.Column(db.Text)
    image = db.Column(db.Text)
    limit = db.Column(db.Text)
    likeco = db.Column(db.Integer)#点赞的数量
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
