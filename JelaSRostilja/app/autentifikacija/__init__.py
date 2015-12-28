from flask import Blueprint

autentifikacija = Blueprint('autentifikacija', __name__)

from . import routes
