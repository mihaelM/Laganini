from flask import render_template, redirect, url_for, request, flash
from .forms import UnosKorisnika
from . import registriranje
from .. import db
from .. models import Korisnik, Uloga

@registriranje.route('/registracija',methods=['GET','POST'])
def registracija():
    form = UnosKorisnika()
    if request.method=='POST':
        if form.validate_on_submit():
            korisnik=Korisnik(ime=form.ime.data,
                              prezime=form.prezime.data,
                              korisnikKorisIme=form.korisIme.data,
                              korisnikPas=form.password.data,
                              uloga=Uloga.query.filter_by(imeUloge=form.uloga.data).first())
            db.session.add(korisnik)
            flash('Novi korisnik uspjesno dodan')
    else:
        return render_template('registriranje/registracija.html',form=form)

    return redirect(url_for('main.ispisi_korisnike'))