from flask import render_template,redirect,url_for,request, flash
from flask.ext.login import current_user
from .forms import UnosDjelatnika,UnosKomentara
from . import main
from .. import db
from ..models import Korisnik,Uloga,Komentar

@main.route('/')
def index():
    Uloga.umetni_uloge()
    return render_template('index.html')


@main.route('/komentari',methods=['GET','POST'])
def komentari():
    form=UnosKomentara()   
    if request.method=='POST':
        if form.validate_on_submit():
            komentar=Komentar(tekstKomentara=form.tekst.data)
            db.session.add(komentar)

            flash('Komentar spjesno objavljen')
            return redirect(url_for('main.komentari'))
    else:
        query = Komentar.query
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Komentar.komentarID.desc()).paginate(page, per_page=100,error_out=False)
    komentari = pagination.items
    return render_template('komentari.html',form=form,pagination=pagination,komentari=komentari)

@main.route('/popis_djelatnika')
def popis_djelatnika():
    query=Korisnik.query
    page = request.args.get('page', 1, type=int)
    pagination = query.filter_by(uloga=Uloga.query.filter_by(imeUloge="Djelatnik").first()).order_by(Korisnik.korisnikID.desc()).paginate(page, per_page=100,error_out=False)
    djelatnici = pagination.items
    return render_template('popis_djelatnika.html',djelatnici=djelatnici,pagination=pagination)

@main.route('/dodaj_djelatnika',methods=['GET','POST'])
def dodaj_djelatnika():
    form=UnosDjelatnika()
    if request.method=='POST':
        if form.validate_on_submit():
            djelatnik=Korisnik(ime=form.ime.data,
                              prezime=form.prezime.data,
                              korisnikKorisIme=form.korisIme.data,
                              korisnikPas=form.password.data,
                              uloga=Uloga.query.filter_by(imeUloge="Djelatnik").first())
            db.session.add(djelatnik)
            flash('Novi djelatnik uspjesno dodan')
    else:
        return render_template('dodaj_djelatnika.html',form=form)

    return redirect(url_for('main.popis_djelatnika'))

@main.route('/korisnik/<int:id>')
def prikazi_korisnika(id):
    korisnik=Korisnik.query.filter_by(korisnikID=id).first()
    return render_template('korisnik.html',korisnik=korisnik,id=korisnik.korisnikID)
