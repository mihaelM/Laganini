from flask import Blueprint

meni = Blueprint('meni', __name__)

from . import routes