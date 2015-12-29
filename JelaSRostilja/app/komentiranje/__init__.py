from flask import Blueprint

komentiranje = Blueprint('komentiranje', __name__)

from . import routes