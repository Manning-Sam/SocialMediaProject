from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import login_manager
from flask_migrate import Migrate

db=SQLAlchemy()
from .blog.routes import blog
from .auth.routes import auth

from .models import User

from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
login = LoginManager()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

app.register_blueprint(blog)
app.register_blueprint(auth)
app.config.from_object(Config)
db.init_app(app)
login.init_app(app)

migrate = Migrate(app,db)
from app import routes
from app import models