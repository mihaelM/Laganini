from flask import Blueprint

main = Blueprint('main', __name__)

from . import routes
from ..models import Dozvole


@main.app_context_processor
def ubaci_dozvole():
    return dict(Dozvole=Dozvole)