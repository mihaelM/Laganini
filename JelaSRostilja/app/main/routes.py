from flask import render_template,redirect,url_for,request, flash
from . import main
from .. import db
from . .models import Korisnik,Uloga,Komentar

@main.route('/')
def index():
    Uloga.umetni_uloge()
    return render_template('index.html')

@main.route('/korisnici')
def ispisi_korisnike():
    query=Korisnik.query
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Korisnik.korisnikID.desc()).paginate(page, per_page=100,error_out=False)
    korisnici = pagination.items
    return render_template('ispisi_korisnike.html',korisnici=korisnici,pagination=pagination)

@main.route('/korisnik/<int:id>')
def prikazi_korisnika(id):
    korisnik=Korisnik.query.filter_by(korisnikID=id).first()
    return render_template('korisnik.html',korisnik=korisnik,id=korisnik.korisnikID)
