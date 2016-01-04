from flask import render_template,redirect,url_for,request, flash
from flask.ext.login import current_user
from .forms import UnosDjelatnika,UnosKomentara,ObrisiDjelatnika,IzmjeniPodatkeRestorana
from . import main
from .. import db
from ..models import Korisnik,Uloga,Komentar,Dozvole,Restoran

@main.route('/',methods=['GET','POST'])
def index():
    restoran=Restoran.query.first()
    form=IzmjeniPodatkeRestorana()
    form.naziv.data=restoran.naziv
    form.adresa.data=restoran.adresa
    form.imeVlas.data=restoran.imeVlas
    form.prezVlas.data=restoran.prezVlas
    form.radnoVrijeme.data=restoran.radnoVrijeme
    form.telefon.data=restoran.telefon
    form.minNarudzba.data=restoran.minNarudzba
    form.proVrijemeDost.data=restoran.proVrijemeDost
    form.nacinPlac.data=restoran.nacinPlac
    form.cijenaDostave.data=restoran.cijenaDostave
    if request.method=='POST':
        restoran.naziv=str(form.naziv.data)
        restoran.adresa=form.adresa.data
        restoran.imeVlas=form.imeVlas.data
        restoran.prezVlas=form.prezVlas.data
        restoran.radnoVrijeme=form.radnoVrijeme.data
        restoran.telefon=form.telefon.data
        restoran.minNarudzba=float(form.minNarudzba.data)
        restoran.proVrijemeDost=form.proVrijemeDost.data       
        restoran.nacinPlac=form.nacinPlac.data
        restoran.cijenaDostave=float(form.cijenaDostave.data)
        restoran.evPopust=bool(form.evPopust.data)
        print(form.naziv.data)
        db.session.commit()

        flash('Podaci uspjesno promjenjeni')
        return redirect(url_for('main.index'))
    return render_template('index.html',form=form,restoran=restoran)


@main.route('/komentari',methods=['GET','POST'])
def komentari():
    form=UnosKomentara()   
    if request.method=='POST':
        if form.validate_on_submit():
            komentar=Komentar(tekstKomentara=form.tekst.data,klijentID=current_user.korisnikID)
            db.session.add(komentar)

            flash('Komentar uspjesno objavljen')
            return redirect(url_for('main.komentari'))
    else:
        query = Komentar.query
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Komentar.komentarID.desc()).paginate(page, per_page=100,error_out=False)
    komentari = pagination.items
    return render_template('komentari.html',form=form,pagination=pagination,komentari=komentari,Korisnik=Korisnik)

@main.route('/popis_djelatnika',methods=['GET','POST'])
def popis_djelatnika():
    form1=ObrisiDjelatnika()
    form2=UnosDjelatnika()
    if request.method=='POST':
        if form1.validate_on_submit():
            djelatnik=Korisnik.query.filter_by(korisnikID=form1.id.data).first()
            db.session.delete(djelatnik)
            db.session.commit()
            flash('Korisnik uspjesno obrisan')
            return redirect(url_for('main.popis_djelatnika'))
        if form2.validate_on_submit():
            djelatnik=Korisnik(ime=form2.ime.data,
                              prezime=form2.prezime.data,
                              korisnikKorisIme=form2.korisIme.data,
                              korisnikPas=form2.password.data,
                              uloga=Uloga.query.filter_by(imeUloge="Djelatnik").first())
            db.session.add(djelatnik)
            flash('Novi djelatnik uspjesno dodan')
            return redirect(url_for('main.popis_djelatnika'))
    query=Korisnik.query
    page = request.args.get('page', 1, type=int)
    pagination = query.filter_by(uloga=Uloga.query.filter_by(imeUloge="Djelatnik").first()).order_by(Korisnik.korisnikID.desc()).paginate(page, per_page=100,error_out=False)
    djelatnici = pagination.items
    return render_template('popis_djelatnika.html',djelatnici=djelatnici,pagination=pagination,form1=form1,form2=form2)

#@main.route('/dodaj_djelatnika',methods=['GET','POST'])
#def dodaj_djelatnika():
#    form=UnosDjelatnika()
#    if request.method=='POST':
#        if form.validate_on_submit():
#            djelatnik=Korisnik(ime=form.ime.data,
#                              prezime=form.prezime.data,
#                              korisnikKorisIme=form.korisIme.data,
#                              korisnikPas=form.password.data,
#                              uloga=Uloga.query.filter_by(imeUloge="Djelatnik").first())
#            db.session.add(djelatnik)
#            flash('Novi djelatnik uspjesno dodan')
#    else:
#        return render_template('dodaj_djelatnika.html',form=form)

#    return redirect(url_for('main.popis_djelatnika'))

@main.route('/korisnik/<int:id>')
def prikazi_korisnika(id):
    korisnik=Korisnik.query.filter_by(korisnikID=id).first()
    return render_template('korisnik.html',korisnik=korisnik,id=korisnik.korisnikID)
