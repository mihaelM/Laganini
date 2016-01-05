import os

class Config:
    DEBUG=True
    SECRET_KEY='hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'baza.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS=True