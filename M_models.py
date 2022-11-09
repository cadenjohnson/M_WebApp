# Script to manage my models (tables in database)
#
#
# Caden Johnson - 5/22/22

from app import db
from datetime import datetime
from time import time
import re
from flask_login import UserMixin


# Class for accounts Database (default)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(100), unique=True)
    email_address = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    #todo = db.relationship('Todo', backref='user', lazy=True)
    # used to create the one-to-many relationships... seems like a lot of unnecessary work rn#############################################################

    # returns a string every time new element is created
    def __repr__(self):
        return '<User %r>' % self.id


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(200), nullable=False)
    #completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # returns a string every time new element is created
    def __repr__(self):
        return '<Task %r>' % self.id


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()

    def slugify(s):
        pattern = r'[^\w+]'
        return re.sub(pattern, '-', s)

    def generate_slug(self):
        if self.title:
            self.slug = self.slugify(self.title)
        else:
            self.slug = str(int(time()))

    def __repr__(self):
        return '<Post %r>' % self.id


class Spotifym(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    refresh_token = db.Column(db.String(500))
    access_token = db.Column(db.String(500))
    expires = db.Column(db.DateTime)
    is_expired = db.Column(db.Boolean)
    scope = db.Column(db.String(300))
    state = db.Column(db.String(8))

    def __repr__(self):
        return '<SpotAcct %r>' % self.id

# more models in temp.txt
