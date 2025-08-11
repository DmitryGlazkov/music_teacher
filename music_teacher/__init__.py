from config import Config
from dotenv import load_dotenv
from flask import Flask
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from .admin import TextDataAdmin, admin
from .models import LearningProcess, LessonPrice, TextData, User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

admin.init_app(app)

admin.add_view(ModelView(LearningProcess, db.session))
admin.add_view(ModelView(LessonPrice, db.session))
admin.add_view(TextDataAdmin(TextData, db.session))

from . import views
