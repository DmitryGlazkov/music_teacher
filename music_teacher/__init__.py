from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager

from dotenv import load_dotenv
from config import Config


load_dotenv()

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from .models import LearningProcess, LessonPrice, TextData, User
from .admin import TextDataAdmin
from .admin import admin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

admin.init_app(app)

admin.add_view(ModelView(LearningProcess, db.session))
admin.add_view(ModelView(LessonPrice, db.session))
admin.add_view(TextDataAdmin(TextData, db.session))

from . import views
