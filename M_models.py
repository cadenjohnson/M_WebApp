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
    # used to create the one-to-many relationships... seems like a lot of unnecessary work rn


    # returns a string every time new element is created
    def __repr__(self):
        return '<User %r>' % self.id


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
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


class SpotifyToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    date_created = db.Column(db.DateTime, default=datetime.now())
    refresh_token = db.Column(db.String(150))
    access_token = db.Column(db.String(150))
    expires_in = db.Column(db.DateTime)
    token_type = db.Column(db.String(50))

    def __repr__(self):
        return '<Token %r>' % self.id

# more models in temp.txt
