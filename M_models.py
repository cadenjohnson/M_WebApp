# Script to manage my models (tables in database)
#
#
# Caden Johnson - 5/22/22

from app import db
from datetime import datetime
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


# more models in temp.txt
