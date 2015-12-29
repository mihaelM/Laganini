from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap
from config import Config


db=SQLAlchemy()
bootstrap = Bootstrap()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'autentifikacija.prijava'

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config())
    
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    wsgi_app = app.wsgi_app

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .meni import meni as meni_blueprint
    app.register_blueprint(meni_blueprint)
    from .autentifikacija import autentifikacija as autentifikacija_blueprint
    app.register_blueprint(autentifikacija_blueprint)
    from .registriranje import registriranje as registriranje_blueprint
    app.register_blueprint(registriranje_blueprint)
    from .komentiranje import komentiranje as komentiranje_blueprint
    app.register_blueprint(komentiranje_blueprint)
    from .narudzba import narudzba as narudzba_blueprint
    app.register_blueprint(narudzba_blueprint)

    return app