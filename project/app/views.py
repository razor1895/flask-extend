# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from models import User, Post, Category, Tag, ROLE_USER, ROLE_ADMIN
from forms import RegisterFrom, LoginForm, PostForm
from hashlib import md5
from config import POSTS_PER_PAGE



@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>', methods = ['GET', 'POST'])
def index(page=1):

    categories = Category.query.all()
    # posts = Post.query.order_by(Post.pub_date.desc()).all()
    # posts = Post.query.order_by(Post.pub_date.desc()).paginate(page, POSTS_PER_PAGE, False).items
    posts = Post.query.order_by(Post.pub_date.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('index.html', posts=posts, categories=categories)

@app.route('/list/<name>')
def list(name):
    categories = Category.query.filter().all()
    for i in categories:
        if i.name == name:
            category = i
            break 
    posts = Post.query.filter_by(category=category).order_by(Post.pub_date.desc()).all()
    return render_template('list.html', categories=categories, category=category, posts=posts)


@app.route('/detail/<id>')
def detail(id):

    categories = Category.query.filter().all()
    post = Post.query.filter_by(id=id).first()
    return render_template('detail.html', categories=categories, post=post)


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():

    form = PostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.data['title']
            body = form.data['body']
            category = form.data['category']
            tags = form.data['tag']
            category = Category.query.filter_by(name=category).first()
            taglist = [Tag(content=tag) for tag in tags.split()]
            try:
                pass
                post = Post(title=title, body=body, category=category, user=current_user,tags=taglist)
                db.session.add(post)
                db.session.commit()
                flash('post successful')
                return redirect(url_for('index'))
            except Exception, e:
                flash('something goes wrong')    
    return render_template('post.html', form=form)

@app.route('/tags')
def tags():

    tags = Tag.query.all()

    return render_template('tags.html', tags=tags)

@app.route('/post/<tag>/<tagid>')
def post_by_tag(tag, tagid):

    tag = Tag.query.filter_by(id=tagid).first()
    posts = tag.posts
    return render_template('post_by_tag.html', posts=posts)


@app.route('/adduser/<nickname>/<email>')
def adduser(nickname, email):
    u = User(nickname=nickname, email=email)
    try:
        db.session.add(u)
        db.session.commit()
        return 'add successful'
    except Exception, e:
        return 'something go wrong'


@app.route('/getuser/<nickname>')
def getuser(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    return render_template('user.html', user=user)


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/account/signup', methods=['GET', 'POST'])
def signup():

    form = RegisterFrom()
    if request.method == 'POST':
        if form.validate_on_submit():
            psdmd5 = md5(form.data['password'])
            password = psdmd5.hexdigest()
            u = User(nickname=form.data['nickname'],
                     email=form.data['email'], password=password)
            try:
                db.session.add(u)
                db.session.commit()
                flash('signup successful')
            except Exception, e:
                return flash('something goes wrong')
            return redirect(url_for('signin'))
    return render_template('signup.html', form=form)


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


@app.route('/account/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            nickname = form.data['nickname']
            psdmd5 = md5(form.data['password'])
            password = psdmd5.hexdigest()
            remember_me = form.data['remember_me']
            user = User.query.filter_by(
                nickname=nickname, password=password).first()
            if user:
                login_user(user, remember=remember_me)
                flash('signin successful')
                return redirect(request.args.get("next") or url_for("index"))
            else:
                flash(u'用户名或者密码错误')

    return render_template('signin.html', form=form)


@app.route('/account/signout')
@login_required
def signout():
    logout_user()
    flash('signout successful')
    return redirect('index')

# @app.route('/account/signin', methods=['GET', 'POST'])
# def signin():
#     form = LoginForm()
#     if request.method == 'POST':
#         if form.validate_on_submit():
#             nickname = form.data['nickname']
#             psdmd5 = md5(form.data['password'])
#             password = psdmd5.hexdigest()
#             u = User.query.filter_by(nickname=nickname, password=password).first()
#             if u:
#                 session['signin'] = True
#                 flash('signin successful')
#                 return redirect(url_for('index'))
#             else:
#                 flash(u'用户名或者密码错误')

#     return render_template('signin.html', form=form)

# @app.route('/account/signout')
# def signout():
#     session.pop('signin', None)
#     flash('signout successful')
#     return redirect('index')
