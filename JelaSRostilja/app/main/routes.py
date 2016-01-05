from flask import render_template,redirect,url_for,request, flash, session
from flask.ext.login import current_user
from .forms import *
from . import main
from .. import db
from ..models import *
from set_up_db import *
import uuid
import os.path
import os

'''
Quote iz knjige => ako zelimo razlikovati narudzbe razlicith kupaca uzimamo ovo u obzir.
The db.session database session is not related to the Flask session
object discussed in Chapter 4. Database sessions are also called transactions.
'''

# TO DO : moramo da mora biti neka kolicina odabrana staviti za broj u formi koliko čega (javascript il nes)
# zapravo, najbolje da to rijesimo preko onih standarnih formi, dakle jelo_opcije.html treba rewrite ili ovo s javascriptom, jQuerryjem

# ovo je kao i konfig, jednom kad smo zadovoljni s BOL-om, stavimo ga na False odmah
BOL = True

# sometimes before_request does not work
# @main.before_request
def before_request():
    global BOL
    if BOL:
         init_insert_into_db()
    BOL = False

    
def handle_sesion_id():
     if  not ('uid' in session):
        session['uid'] = str(uuid.uuid4())

# činjenica je da, ovo bi trebali inace radit u ovom before_requestu (i bazu i handlanje session_id-a), ali on nekad bugga
# jer sto ako nam prvo izvedena naredba ne bude ta koja odlazi na index page (mozemo mozda u tom slucaju redirekciju implementirati)
# ili ovo dvoje cp-ati u svaku naredbu route, al to je malo glupo al sta je tu je

@main.route('/',methods=['GET','POST'])
def index():
    before_request() # ono kad sam implementiras binarne semafore
    handle_sesion_id()
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


@main.route('/meni', methods=['GET'])
def prikazi_meni():

    page = request.args.get('page', 1, type=int)
    jela = Jelo.query.order_by(Jelo.jeloID.asc()).paginate(page, per_page=100,error_out=False).items
    # tu mozda jos queryjat (ili u modelu podataka po kategorijama)
    return render_template('meni.html', jela = jela)

@main.route('/meni/<int:id>', methods=['GET'])
def prikazi_jelo(id): # ukljucujuci opcije
    jelo = Jelo.query.filter_by(jeloID=id).first()
    my_string = os.getcwd() + '/app/static/img/' + jelo.fotoJeloIme #sad ovo mi se ne svidja bas, al eto
  
    print(my_string)
    exist = os.path.exists(my_string)

    # fino je sve u jelo.opcije
    return render_template('jelo_opcije.html', jelo = jelo, exist = exist)

@main.route('/meni', methods=['POST'])
def dodaj_u_kosaricu(): #ovo je id od jela
    
    jeloID = request.form.get('jeloID')

    jelo = Jelo.query.filter_by(jeloID=jeloID).first()

    opcija = None
    if jelo.opcije:
         opcija = request.form.get( 'opcija' )

    kolicina = request.form.get( 'kolicina' )
  #  print (kolicina)
    
    jeloKosarica = JeloKosarica ( 
        jeloID = jelo.jeloID,
        naziv = jelo.naziv,
        fotoJeloIme = jelo.fotoJeloIme,
        cijena = jelo.cijena, 
        dostupnost = jelo.dostupnost, 
        cestoNarucivano = jelo.cestoNarucivano,
        kategorijaID = jelo.kategorijaID,
        opcija = opcija,
        kolicina = kolicina,
        sessionID = session['uid']
        # opcije =  db.relationship("Opcija", secondary=Jelo_Ima_Opcija, back_populates="jela"), kasnije popunimo ju
    )

    db.session.add(jeloKosarica)

    # cp od onog sto radimo u prikazi meni, ?
    page = request.args.get('page', 1, type=int)
    jela = Jelo.query.order_by(Jelo.jeloID.asc()).paginate(page, per_page=100,error_out=False).items
    # tu mozda jos queryjat (ili u modelu podataka po kategorijama)
    return render_template('meni.html', jela = jela)


def prikaz():
    jelaKosarica=JeloKosarica.query.filter_by(sessionID=session['uid'])
    totalCijena = 0

    for jeloKosarica in jelaKosarica:
       totalCijena += jeloKosarica.cijena*jeloKosarica.kolicina

    return render_template('kosarica.html', jelaKosarica = jelaKosarica, totalCijena = totalCijena)

@main.route('/kosarica', methods=['GET'])
def prikazi_kosaricu():
    #prikazuje jela iz baze jeloKosarica
    return prikaz()
    

@main.route('/kosarica/promijeni_broj', methods=['POST']) #post je kratica za mućki iza leđa
def promijeni_broj():
    #prikazuje jela iz baze jeloKosaricaj
    jeloKosarica=JeloKosarica.query.filter_by(jeloKosaricaID = request.form.get('jeloID')).first()
    jeloKosarica.setKolicina( int( request.form.get('kolicina') ))

    return prikaz()

@main.route('/kosarica/izbrisi', methods=['POST']) #post je kratica za mućki iza leđa
def izbrisi():
    #prikazuje jela iz baze jeloKosaricaj
    jeloKosarica=JeloKosarica.query.filter_by(jeloKosaricaID = request.form.get('jeloID')).first()
    db.session.delete(jeloKosarica)

    return prikaz()

# nisam radio potvrdu na 'normalan' nacin s wtf-om jer cim mi se ucita forma odmah je post, pa tu nesto steka ()

@main.route('/kosarica/potvrda', methods = ['POST']) 
def potvrdi_kosaricu():
    #samo redirect na unos podataka o narurzbi
    form = PodaciNarudzbe()
    # treba izbrisati sadržaj košarice
    return render_template('podatci_narudzba.html', form=form)

@main.route('/kosarica/potvrdjena', methods = ['POST']) 
def potvrdjena_kosarica():
    #di je sad validate on submit??
   # print (form.adresa.data) radi
    jelaKosarica=JeloKosarica.query.filter_by(sessionID=session['uid'])

    opisNarudzbe = ""
    totalCijena = 0

    for jeloKosarica in jelaKosarica:
       totalCijena += jeloKosarica.cijena*jeloKosarica.kolicina
       opisNarudzbe+=str(jeloKosarica)+"\n"

    #print(opisNarudzbe) # za provjeru
   # print(totalCijena)

    form = PodaciNarudzbe()

    narudzba = Narudzba(
    adresa = form.adresa.data,
    kat=form.kat.data,
    kontakt_broj=form.kontakt_broj_mob.data,
    email=form.email.data,
    placanje=form.uloga.data, # ovo je trebalo biti placanje lol
    opisNarudzbe = opisNarudzbe
    )
   
    # e sad je pravo vrijeme za izbrisat trentunu kosaricu
    JeloKosarica.query.filter_by(sessionID=session['uid']).delete()
    

    return render_template('uspjesna_narudzba.html') # tu jos sad treba dodat sav data o naruzbi, ili ne ugl nes u tom stilu da ovi mogu potvrdit


    
