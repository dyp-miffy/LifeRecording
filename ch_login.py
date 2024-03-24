from functools import wraps
from flask import session,render_template

def is_login(func):
    @wraps(func)
    def check_login(*args,**kwargs):
        user=session.get('user')
        if user:
            return func(*args,**kwargs)
        else:
            return render_template('login.html',msg='没登录请登录')
    return check_login