#配置类
class Config(object):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/liferecording"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # 会打印原生sql语句，便于观察测试
    SECRET_KEY="123456"