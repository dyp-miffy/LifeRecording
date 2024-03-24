import os.path
import time
from multiprocessing.connection import Client

from flask import Flask, redirect, render_template, session, request, jsonify
from werkzeug.utils import secure_filename

from ch_login import is_login
from config import Config
from db import db
from models.diary import Diary
from models.user import User
from models.userlike import Userlike


UPLOAD_FOLDER = 'D:/flaskProject/LifeRecording/static/'

app = Flask(__name__)
# 引入配置文件
app.config.from_object(Config)
# 把flask对象app初始化在db对象中
db.init_app(app)
# app对象在整个项目上下文中生效
app.app_context().push()

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 退出系统
@app.route('/out')
def out():
    # 删除session中key为user的信息
    session.pop('user')
    # 重定向到路由地址为login的视图函数
    return redirect('/')


# 登录
@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login_name = request.form['login_name']
        login_password = request.form['login_password']
        user = User.query.filter_by(name=login_name).first()
        if user:
            if user.password == login_password:
                session['user'] = login_name
                return redirect('/index')
                # return render_template('index.html')
            else:
                return render_template('login.html', msg='密码输入不正确！')
        else:
            return render_template('login.html', msg='用户不存在！')


# 注册
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        signup_name = request.form['signup_name']
        signup_password = request.form['signup_password']
        signup_password_confirm = request.form['signup_password_confirm']
        # 判断用户名是否已存在
        user = User.query.filter_by(name=signup_name).first()
        if user:  # 用户名已存在
            return render_template('login.html', msg='用户名已被注册')
        else:
            new_user = User(name=signup_name, password=signup_password)
            # 用户名不存在，则判断密码和确认密码是否相同
            if signup_password == signup_password_confirm:
                db.session.add(new_user)
                db.session.commit()
                return render_template('login.html', msg='注册成功')
            else:  # 密码和确认密码不同
                return render_template('login.html', msg='再次确认密码')


@app.route('/index')
@is_login
def index():
    username = session['user']
    user = User.query.filter(User.name == username).first()
    # sqlalchemy：从数据库中查询所有的记录
    user_id = user.id
    records = Diary.query.filter_by(limit='公开可见').all()
    # 渲染记录列表页面目标文件，传入records参数
    return render_template('index.html', username=username, records=records, user_id=user_id)


@app.route('/zan', methods=['POST'])
@is_login
def zan():
    likeco = request.json.get("likeco")
    is_like = request.json.get("is_like")
    diary_id = request.json.get("recordid")

    username = session['user']
    user = User.query.filter(User.name == username).first()
    records = Diary.query.filter_by(limit=1).all()
    user1_id = user.id
    userl = Userlike.query.filter(Userlike.user_id == user1_id, Userlike.diary_id == diary_id).first()

    if userl:
        Userlike.query.filter(Userlike.user_id == user1_id, Userlike.diary_id == diary_id).update({'is_like': is_like})
        db.session.commit()

    else:
        userlike = Userlike(user_id=user.id, diary_id=diary_id, is_like=is_like)
        # 调用添加操作
        db.session.add(userlike)
        db.session.commit()

    record = Diary.query.filter(Diary.id == diary_id).first()
    Diary.query.filter(Diary.id == diary_id).update({'likeco': likeco})
    db.session.commit()
    print("返回到前端时的点赞数：")
    print(record.likeco)
    dict = {'likeco2': record.likeco, 'is_like2': is_like}
    return jsonify(dict)


# 添加记录
@app.route('/form', methods=['GET', 'POST'])
@is_login
def form():
    username = session['user']
    user = User.query.filter(User.name == username).first()
    print(user)
    if request.method == 'GET':
        return render_template('form.html', username=username)
    else:
        # 从表单请求体中获取请求数据
        content = request.form['content']
        mood = request.values.get('mood')
        lim = request.values.get('limit')
        f = request.files['file']
        filename = secure_filename(f.filename)
        fi = '/static/' + filename
        if filename:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # if lim == '公开可见':
        #     limit = 1
        # else:
        #     limit = 0
        # 获取时间
        t = time.localtime()
        # current_time = time.strftime("%Y-%m-%d", t)
        user_id = user.id
        # 创建一个记录对象
        record = Diary(date=t, text=content, mood=mood, image=fi, user_id=user_id, limit=lim, likeco=0)
        # 调用添加操作
        db.session.add(record)
        # 必须提交才能生效
        db.session.commit()
        # 创建完成后重定向到记录列表页面
        return redirect('/ui-elements')


# 记录列表
@app.route('/ui-elements')
@is_login
def lists():
    username = session['user']
    user = User.query.filter(User.name == username).first()
    # sqlalchemy：从数据库中查询所有的记录
    user_id = user.id
    records = Diary.query.filter_by(user_id=user_id).all()
    # 渲染记录列表页面目标文件，传入records参数
    return render_template('ui-elements.html', username=username, records=records)


# 记录详情
@app.route('/record_detail')
@is_login
def detail():
    username = session['user']
    user = User.query.filter(User.name == username).first()
    id = int(request.args.get("id"))
    record = Diary.query.get(id)

    user1_id = user.id
    userl = Userlike.query.filter(Userlike.user_id == user1_id, Userlike.diary_id == record.id).first()

    if userl:
        print("已存在")
    else:
        a = 0
        userlike = Userlike(user_id=user1_id, diary_id=record.id, is_like=a)
        # 调用添加操作
        db.session.add(userlike)
        db.session.commit()
        userl = userlike

    # userl = Userlike.query.filter(Userlike.user_id == user1_id, Userlike.diary_id == record.id).first()

    # 渲染记录详情页面
    return render_template('detail.html', username=username, record=record, userl=userl)


# 柱状统计图
@app.route('/bar')
@is_login
def bar():
    username = session['user']
    return render_template('bar.html', username=username)


# 饼状统计图
@app.route('/pie')
@is_login
def pie():
    username = session['user']
    return render_template('pie.html', username=username)


# 接收数据库传来的数据传给前端（bar.html)
@app.route('/get_bar_data')
@is_login
def get_bar_data():
    username = session['user']
    user = User.query.filter(User.name == username).first()
    # sqlalchemy：从数据库中查询所有的记录
    user_id = user.id
    records = Diary.query.filter_by(user_id=user_id).all()
    moodlist = ['happy', 'so-so', 'bad']
    countlist = []
    a = 0
    b = 0
    c = 0
    for diary in records:
        if diary.mood == 'happy':
            a = a + 1
        elif diary.mood == 'so-so':
            b = b + 1
        else:
            c = c + 1
    countlist.append(a)
    countlist.append(b)
    countlist.append(c)
    # 定义字典
    dict = {'mood': moodlist, 'count': countlist}
    print(dict)
    return jsonify(dict)


# 更改
@app.route('/update', methods=['GET', 'POST'])
@is_login
def update():
    if request.method == 'GET':
        # 根据id查询
        id = int(request.args.get("id"))
        record = Diary.query.get(id)
        # print(record)
        return render_template('update.html', record=record)
    else:
        # 获取内容
        content = request.form['content']
        mood = request.values.get('mood')
        id = int(request.form['id'])
        limit = request.values.get('limit')
        f = request.files['file']
        filename = secure_filename(f.filename)
        # pa = 'D:/flaskProject/LifeRecording/static/'+filename
        if filename:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        fi = '/static/'+filename
        # 获取时间
        t = time.localtime()
        Diary.query.filter_by(id=id).update({'text': content, 'mood': mood, 'image': fi, 'date': t, 'limit': limit})
        # 提交才能生效
        db.session.commit()
        return redirect('/ui-elements')


# 删除
@app.route('/delete')
@is_login
def delete():
    id = int(request.args.get("id"))
    record = Diary.query.get(id)
    # print(record)
    db.session.delete(record)
    db.session.commit()
    return redirect('/ui-elements')


# 关于我们
@app.route('/contact_us')
def contact():
    username = session['user']
    return render_template('contact_us.html', username=username)


if __name__ == '__main__':
    app.run()
