from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required,current_user
from . import autentifikacija
from .. import db
from ..models import Korisnik,Uloga
from .forms import PrijavaKorisnika,RegistracijaKorisnika

@autentifikacija.route('/prijava',methods=['GET', 'POST'])
def prijava():
    form=PrijavaKorisnika()
    if form.validate_on_submit():
        korisnik = Korisnik.query.filter_by(korisnikKorisIme=form.username.data).first()
        if korisnik is not None and korisnik.provjeri_password(form.password.data):
            login_user(korisnik)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Pogresno korisnicko ime ili lozinka.')
    return render_template('autentifikacija/prijava.html', form=form)

@autentifikacija.route('/odjava')
def odjava():
    logout_user()
    flash('Uspjesno ste odjavljeni iz sustava.')
    return redirect(url_for('main.index'))

@autentifikacija.route('/registracija',methods=['GET', 'POST'])
def registracija():
    form=RegistracijaKorisnika()
    if form.validate_on_submit():
        if(Korisnik.query.filter_by(korisnikKorisIme=form.korisIme.data).first() is not None):
            flash('Korisnicko ime vec postoji')
            return redirect(url_for('autentifikacija.registracija'))
        korisnik=Korisnik(ime=form.ime.data,
                              prezime=form.prezime.data,
                              korisnikKorisIme=form.korisIme.data,
                              korisnikPas=form.password.data,
                              uloga=Uloga.query.filter_by(imeUloge="Korisnik").first())
        db.session.add(korisnik)
        flash('Novi korisnik uspjesno dodan')
        login_user(Korisnik.query.filter_by(korisnikKorisIme=korisnik.korisnikKorisIme).first())
        return redirect(url_for('main.index'))
    return render_template('autentifikacija/registracija.html',form=form)
