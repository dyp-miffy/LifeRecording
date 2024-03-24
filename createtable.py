from app import app
from db import db
from models.diary import Diary
from models.userlike import Userlike
from models.like import Like
from models.user import User
#把flask对象app初始化在db对象中
db.init_app(app)
#app对象在整个项目上下文中生效
app.app_context().push()
# 根据类中继承自db.Model的模型类创建表
db.drop_all()
db.create_all()

