# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import basedir

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "signin"
login_manager.login_message = u"Bonvolu ensaluti por uzi tio paĝo."

# from app import views, models
import views, models