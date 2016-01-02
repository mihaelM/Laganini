from flask import render_template,redirect,url_for,request, flash, session
from .forms import *
from . import main
from .. import db
from ..models import *
from set_up_db import *
import uuid

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

@main.route('/')
def index():
    before_request() # ono kad sam implementiras binarne semafore
    handle_sesion_id()
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

@main.route('/korisnici')
def ispisi_korisnike():
    query=Korisnik.query
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Korisnik.korisnikID.desc()).paginate(page, per_page=100,error_out=False)
    korisnici = pagination.items
    return render_template('ispisi_korisnike.html',korisnici=korisnici,pagination=pagination)

@main.route('/dodaj_korisnika',methods=['GET','POST'])
def dodaj_korisnika():
    form=UnosKorisnika()
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
        return render_template('dodaj_korisnika.html',form=form)

    return redirect(url_for('main.ispisi_korisnike'))

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
    # fino je sve u jelo.opcije
    return render_template('jelo_opcije.html', jelo = jelo)

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


@main.route('/kosarica', methods=['GET'])
def prikazi_kosaricu():
    #prikazuje jela iz baze jeloKosarica
    jelaKosarica=JeloKosarica.query.filter_by(sessionID=session['uid'])
    return render_template('kosarica.html', jelaKosarica = jelaKosarica)


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
  # e sad je pravo vrijeme za izbrisat trentunu kosaricu
    JeloKosarica.query.filter_by(sessionID=session['uid']).delete()

    return render_template('uspjesna_narudzba.html') # tu jos sad treba dodat sav data o naruzbi, ili ne ugl nes u tom stilu da ovi mogu potvrdit


    
