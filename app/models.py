import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login

# Два уровня секретности:
ROLE_STUDENT = 0
ROLE_TEACHER = 1


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(64), index=True, unique=True)
    email = db.Column(db.VARCHAR(128), index=True, unique=True)
    password = db.Column(db.String(256))
    first_name = db.Column(db.VARCHAR(64))
    last_name = db.Column(db.VARCHAR(64))
    role = db.Column(db.SmallInteger, default=ROLE_STUDENT)
    posts = db.relationship('Post', backref='user_id', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_teacher_role(self):
        self.role = ROLE_TEACHER


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)  # Время создания поста
    status = db.Column(db.Integer, default=0)  # Статус, показывающий, был ли пост отредактирован
    name = db.Column(db.VARCHAR(64))
    text = db.Column(db.String(1024))
    level = db.Column(db.SmallInteger, default=ROLE_STUDENT)
    author = db.Column(db.Integer, db.ForeignKey('user.id'))

    def set_timestamp(self):
        self.timestamp = datetime.datetime.now()

    def set_changed_status(self):
        self.status = 1

    def set_name(self, name):
        self.name = name

    def set_text(self, text):
        self.text = text

    def set_level(self, lvl):
        self.level = ROLE_STUDENT if lvl is False else ROLE_TEACHER

    def set_author(self, author_id):
        self.author = author_id
