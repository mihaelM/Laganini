from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required,current_user
from . import autentifikacija
from .. import db
from ..models import Korisnik
from .forms import PrijavaKorisnika

@autentifikacija.route('/prijava',methods=['GET', 'POST'])
def prijava():
    form=PrijavaKorisnika()
    if form.validate_on_submit():
        korisnik = Korisnik.query.filter_by(korisnikKorisIme=form.username.data).first()
        if korisnik is not None and korisnik.provjeri_password(form.password.data):
            login_user(korisnik)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('autentifikacija/prijava.html', form=form)

@autentifikacija.route('/odjava')
def odjava():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
