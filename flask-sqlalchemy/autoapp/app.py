# -*- coding: utf-8 -*-
                               
from flask import Flask
from database import init_db, db_session
from models import User
                               
app = Flask(__name__)
                               
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
                               
                               
@app.route('/')
def index():
    return 'hello world flask'
                               
@app.route('/add/<name>/<email>')
def add(name, email):
    u = User(name=name, email=email)
    try:
        db_session.add(u)
        db_session.commit()
    except Exception, e:
        return 'wrong'
    return 'Add %s user successfully' % name
                               
@app.route('/get/<name>')
def get(name):
    try:
        u = User.query.filter(User.name==name).first()
    except Exception, e:
        return 'there isnot %s' % name
    return 'hello %s' % u.name
                               
if __name__ == '__main__':
    init_db()
    app.debug = True
    app.run()