from flask_sqlalchemy import SQLAlchemy
# 此时先不传入app，避免循环导入

db = SQLAlchemy() # 创建一个SQLAlchemy对象