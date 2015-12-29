from flask import render_template, redirect, url_for, request, flash
from . import meni
from .. import db
from . .models import Korisnik, Jelo

@meni.route('/meni')
def meni():
    query = Jelo.query
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Jelo.jeloID.desc()).paginate(page, per_page=100, error_out = False)
    jela = pagination.items
    return render_template('meni/meni.html', jela = jela, pagination = pagination)

