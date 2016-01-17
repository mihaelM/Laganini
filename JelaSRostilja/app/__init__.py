from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from config import Config
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')


db=SQLAlchemy()
bootstrap = Bootstrap()
mail = Mail()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'autentifikacija.prijava'

def create_app():

    app = Flask(__name__)
    #morao malo na gmailu poradit3
    app.config.update(dict(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'www.mihael@gmail.com',
    MAIL_PASSWORD = '55555 As',
   ))

    mail.init_app(app)

    app.config.from_object(Config())
    
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    wsgi_app = app.wsgi_app

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .autentifikacija import autentifikacija as autentifikacija_blueprint
    app.register_blueprint(autentifikacija_blueprint)

    return app