

import os

BASE_DIR = os.path.dirname(os.path.abspath(__name__))

class Config:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
    SECRET_KEY = 'WUBULUBADUBDUB'
    SESSION_COOKIE_NAME = 'McKrakens Cookie'
