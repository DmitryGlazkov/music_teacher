from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from . import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class LearningProcess(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    text = db.Column(db.String(500), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    added_by = db.Column(db.String(64))    

    def __repr__(self):  
        return f'<LearningProcess {self.id}: {self.text}>'


class LessonPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lesson_name = db.Column(db.String(100), nullable=False)
    price_duration = db.Column(db.String, nullable=True)
    comment = db.Column(db.String(100), nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    added_by = db.Column(db.String(64))

    def __repr__(self):  
        return f'<LessonPrice {self.lesson_name}: {self.price_duration} {self.comment}>'
    

class TextData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    added_by = db.Column(db.String(64))

    def __repr__(self):  
        return f'<TextData {self.title}: {self.text}>'
