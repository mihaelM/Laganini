from flask import render_template,redirect,url_for,request, flash
from .forms import UnosKorisnika
from . import main
from .. import db
from ..models import Korisnik,Uloga

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/korisnici')
def ispisi_korisnike():
    users=[]

    try:
        for i in db.session.query(Korisnik):
            users.append(i)
    except:
        pass
    return render_template('ispisi_korisnike.html',users=users)

@main.route('/dodaj_korisnika',methods=['GET','POST'])
def dodaj_korisnika():
    form=UnosKorisnika()
    if request.method=='POST':
        if form.validate_on_submit():
            podaci=dict(ime=form.ime.data,username=form.korisIme.data,prezime=form.prezime.data,password=form.password.data)
            Korisnik.dodajKorisnika(**podaci)
            print(podaci)
            flash('Novi korisnik uspjesno dodan')
    else:
        return render_template('dodaj_korisnika.html',form=form)

    return redirect(url_for('main.ispisi_korisnike'))

@main.route('/korisnik/<int:id>')
def prikazi_korisnika(id):
    korisnik=Korisnik.query.filter_by(korisnikID=id).first()
    return render_template('korisnik.html',korisnik=korisnik,id=korisnik.korisnikID)
