from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_migrate import Migrate
from os import path
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app,db)
DB_NAME = "database.db"

from app import views, models, auth

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')

from .models import User

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# ______________________________