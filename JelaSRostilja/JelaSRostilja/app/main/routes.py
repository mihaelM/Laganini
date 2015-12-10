from flask import render_template,redirect,url_for,request
from .forms import NameForm
from . import main
from .. import db
from ..models import Korisnik

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/korisnici',methods=['GET','POST'])
def ispisi_korisnike():
    users=[]
    form=NameForm()
    
    if request.method=='POST':
        if form.validate_on_submit():
            Korisnik.dodajKorisnika(form.korisIme.data)

    try:
        for i in db.session.query(Korisnik):
            users.append(i)
    except:
        pass
    return render_template('ispisi_korisnike.html',users=users,form=form)
