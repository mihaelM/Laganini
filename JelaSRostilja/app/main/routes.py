from flask import render_template,redirect,url_for,request, flash, session, make_response
from flask.ext.login import current_user
import smtplib
from error_handle import *
from .forms import *
from . import main
from .. import db
from ..models import *
from set_up_db import *
from sendmail import *
from statistics import *
import uuid
import os.path
import os
from wtforms import ValidationError
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
    if request.method=='GET':
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
        db.session.commit()

        flash('Podaci uspješno promjenjeni')
        return redirect(url_for('main.index'))
    return render_template('index.html',form=form,restoran=restoran,ocjena=Restoran.izracunaj_ocjenu())



@main.route('/komentari',methods=['GET','POST'])
def komentari():
    form=UnosKomentara()
    form2=UnosOcjene() 
    if request.method=='POST':
        if form.validate_on_submit():
            komentar=Komentar(tekstKomentara=form.tekst.data,klijentID=current_user.korisnikID)
            db.session.add(komentar)

            flash('Komentar uspješno objavljen')
            return redirect(url_for('main.komentari'))
        else:
            current_user.ocjena=form2.ocjena.data
            db.session.commit()
            return redirect(url_for('main.komentari'))
    query = Komentar.query
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Komentar.komentarID.desc()).paginate(page, per_page=100,error_out=False)
    komentari = pagination.items
    return render_template('komentari.html',form=form,form2=form2,pagination=pagination,komentari=komentari,Korisnik=Korisnik)


@main.route('/popis_djelatnika',methods=['GET','POST'])
def popis_djelatnika():
    form1=ObrisiDjelatnika()
    form2=UnosDjelatnika()
    if request.method=='POST':
        if form1.validate_on_submit():
            djelatnik=Korisnik.query.filter_by(korisnikID=form1.id.data).first()
            db.session.delete(djelatnik)
            db.session.commit()
            flash('Djelatnik uspješno obrisan')
            return redirect(url_for('main.popis_djelatnika'))
        if form2.validate_on_submit():
            if(Korisnik.query.filter_by(korisnikKorisIme=form2.korisIme.data).first() is not None):
                flash('Korisničko ime već postoji')
                return redirect(url_for('main.popis_djelatnika'))
            djelatnik=Korisnik(ime=form2.ime.data,
                              prezime=form2.prezime.data,
                              korisnikKorisIme=form2.korisIme.data,
                              korisnikPas=form2.password.data,
                              uloga=Uloga.query.filter_by(imeUloge="Djelatnik").first())
            db.session.add(djelatnik)
            flash('Novi djelatnik uspješno dodan')
            return redirect(url_for('main.popis_djelatnika'))
    query=Korisnik.query
    page = request.args.get('page', 1, type=int)
    pagination = query.filter_by(uloga=Uloga.query.filter_by(imeUloge="Djelatnik").first()).order_by(Korisnik.korisnikID.desc()).paginate(page, per_page=100,error_out=False)
    djelatnici = pagination.items
    return render_template('popis_djelatnika.html',djelatnici=djelatnici,pagination=pagination,form1=form1,form2=form2)


@main.route('/korisnik/<int:id>')
def prikazi_korisnika(id):
    korisnik=Korisnik.query.filter_by(korisnikID=id).first()
    return render_template('korisnik.html',korisnik=korisnik,id=korisnik.korisnikID)


@main.route('/meni', methods=['POST','GET'])
def prikazi_meni():
    form2=IzbrisiKategoriju()
    form3=DodajKategoriju()
    kategorije=Kategorija.query.all()
    if request.method=='POST':
        if form2.kategorijaID.data.isalnum():
            print("test")
            kategorija=Kategorija.query.filter_by(kategorijaID=form2.kategorijaID.data).first()
            for j in kategorija.jela:
                db.session.delete(j)
            db.session.delete(kategorija)
            db.session.commit()
            flash('Kategorija obrisana')
            return redirect(url_for('main.prikazi_meni'))
        elif form3.kategorijaIme.data.isalnum():
            novaKategorija=Kategorija()
            novaKategorija.kategorijaIme=form3.kategorijaIme.data
            print(novaKategorija)
            db.session.add(novaKategorija)
            db.session.commit()
            flash('Kategorija dodana')
            return redirect(url_for('main.prikazi_meni'))
    page = request.args.get('page', 1, type=int)
    form = IzbrisiJelo()
    jela = Jelo.query.order_by(Jelo.jeloID.asc()).paginate(page, per_page=100,error_out=False).items
    # tu mozda jos queryjat (ili u modelu podataka po kategorijama)
    return render_template('meni.html', jela = jela, form = form, form2=form2,form3=form3,kategorije=kategorije)


@main.route('/brisi', methods=['POST'])
def brisi_jelo():
    
    jeloID = request.form.get('jeloID')
    jelo = Jelo.query.filter_by(jeloID = request.form.get('jeloID') ).first()
    db.session.delete(jelo)
    form = IzbrisiJelo()

    page = request.args.get('page', 1, type=int)
    jela = Jelo.query.order_by(Jelo.jeloID.asc()).paginate(page, per_page=100,error_out=False).items
    # tu mozda jos queryjat (ili u modelu podataka po kategorijama)
    return render_template('meni.html', jela = jela, form = form)

@main.route('/meni/<int:id>', methods=['POST','GET'])
def prikazi_jelo(id): # ukljucujuci opcije
    form2=IzmjeniDostupnost()
    
    jelo = Jelo.query.filter_by(jeloID=id).first()
    if request.method=='POST':
        if form2.validate_on_submit():
            jelo.dostupnost=not jelo.dostupnost
            db.session.commit()
            flash('Dostupnost uspješno promjenjena')
            return redirect(url_for('main.prikazi_jelo',id=id))
        else:
            pass
    print("test")
    my_string = os.getcwd() + '/app/static/img/' + jelo.fotoJeloIme #sad ovo mi se ne svidja bas, al eto
  
    print(my_string)
    exist = os.path.exists(my_string)

    form1 = JeloForm()

    # fino je sve u jelo.opcije
    return render_template('jelo_opcije.html', jelo = jelo, exist = exist, form1 = form1, form2 = form2)

@main.route('/meni', methods=['GET','POST'])
def dodaj_u_kosaricu(): #ovo je id od jela
    form1 = JeloForm()

    jeloID = request.form.get('jeloID')

    jelo = Jelo.query.filter_by(jeloID=jeloID).first()

    opcija = None
    if jelo.opcije:
         opcija = request.form.get( 'opcija' )

    kolicina = int( form1.kolicina.data )
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
    print(jeloKosarica)
    db.session.add(jeloKosarica)

    # cp od onog sto radimo u prikazi meni, ?
    
    page = request.args.get('page', 1, type=int)
    jela = Jelo.query.order_by(Jelo.jeloID.asc()).paginate(page, per_page=100,error_out=False).items
    # tu mozda jos queryjat (ili u modelu podataka po kategorijama)
    return render_template('meni.html', jela = jela)


def prikaz():
    form1 = KosaricaForm()
    form2 = IzbrisiJelo()
    form3 = PotvrdiKosaricu()

    jelaKosarica=JeloKosarica.query.filter_by(sessionID=session['uid'])
    totalCijena = 0.0

    for jeloKosarica in jelaKosarica:
       totalCijena += jeloKosarica.cijena*jeloKosarica.kolicina

    minNarudzba= Restoran.query.first().minNarudzba
    cijenaDostave = Restoran.query.first().cijenaDostave

    return render_template('kosarica.html', cijenaDostave = cijenaDostave,
                           minNarudzba = minNarudzba, jelaKosarica = jelaKosarica, totalCijena = totalCijena, form1 = form1, form2 = form2, form3 = form3)

@main.route('/kosarica', methods=['GET'])
def prikazi_kosaricu():
    #prikazuje jela iz baze jeloKosarica
    return prikaz()
    
#    form = RegistrationForm(request.POST) lol ima to



@main.route('/kosarica/promijeni_broj', methods=['POST']) #post je kratica za mućki iza leđa
def promijeni_broj():
    #prikazuje jela iz baze jeloKosaricaj
    form1 = KosaricaForm(request.form) #request.form.get('jeloID')
    if form1.validate_on_submit():
         jeloKosarica=JeloKosarica.query.filter_by(jeloKosaricaID = request.form.get('jeloID') ).first()
         jeloKosarica.setKolicina( int( form1.kolicina.data ) )
         return prikaz()
    else:
         return prikaz() #sad konačno možemo i na frontendu (javascript) i backendu rješavati fillanje formi

@main.route('/kosarica/izbrisi', methods=['POST']) #post je kratica za mućki iza leđa
def izbrisi():
    #prikazuje jela iz baze jeloKosaricaj
    jeloKosarica=JeloKosarica.query.filter_by(jeloKosaricaID = request.form.get('jeloID')).first()
    db.session.delete(jeloKosarica)

    return prikaz()

# nisam radio potvrdu na 'normalan' nacin s wtf-om jer cim mi se ucita forma odmah je post, pa tu nesto steka ()

@main.route('/kosarica/potvrda', methods = ['GET','POST']) 
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

    cijenaDostave=Restoran.query.first().cijenaDostave

    opisNarudzbe = ""
    cijenaHrane = 0.0

    i = 0
    for jeloKosarica in jelaKosarica:
       cijenaHrane += jeloKosarica.cijena * jeloKosarica.kolicina
       if i == 0:
            opisNarudzbe+= repr(jeloKosarica)
            i+=1
       else:
           opisNarudzbe+= " | " + repr(jeloKosarica)

    #print(opisNarudzbe) # za provjeru

    form = PodaciNarudzbe()
    if form.validate_on_submit():
        print("val")
        narudzba = Narudzba(
        adresa = form.adresa.data,
        kat=form.kat.data,
        kontakt_broj=form.kontakt_broj_mob.data,
        email=form.email.data,
        placanje=form.uloga.data, # ovo je trebalo biti placanje lol
        opisNarudzbe = opisNarudzbe.decode('utf-8'), #ovo radi na neku foru
        narudzbaCijenaDostave = cijenaDostave,
        cijenaHrane = cijenaHrane
        )

        db.session.add(narudzba) # dodavanje u bazu
   
        #novo
        for jeloKosarica in jelaKosarica:
            for i in xrange(0, int(jeloKosarica.kolicina)):
                stats = NarudzbaStatistika (
                    narudzbaID = narudzba.narudzbaID,
                    jeloID = jeloKosarica.jeloID,
                    cijena = jeloKosarica.cijena
                )
                db.session.add(stats)


        # e sad je pravo vrijeme za izbrisat trentunu kosaricu
        JeloKosarica.query.filter_by(sessionID=session['uid']).delete()
        return render_template('uspjesna_narudzba.html')
        
    else:
        for error in form.errors:
            flash(form.errors[error][0])
        return redirect(url_for('main.potvrdi_kosaricu'))
    

    

def prikaz_narudzbi():
    narudzbe = Narudzba.query.order_by(Narudzba.narudzbaID.desc()) #ovaj paginate bas 
    formPotvrda = DjelatnikPotvrdi()
    formIzbrisi = DjelatnikBrisi() #ako obriše narudžba prihvaća 
    formIzlistaj = DjelatnikSnimi()
    djelatnik = ucitaj_korisnika(current_user.get_id())
    return render_template ('narudzbe.html', narudzbe = narudzbe, djelatnik = djelatnik, formPotvrda = formPotvrda, formIzbrisi = formIzbrisi, formIzlistaj = formIzlistaj)

@main.route('/narudzbe',  methods = ['GET'])
def prikazi_narudzbe():
    return prikaz_narudzbi()
    
@main.route('/narudzbe/spremi',  methods = ['POST']) #u predifiniranu tekstualnu datoteku
def spremi_u_tekst_fajl():
    narudzba=Narudzba.query.filter_by(narudzbaID = request.form.get('narudzbaID')).first()

    filename = 'myfile' + str(narudzba.narudzbaID) + '.txt'
    f = open(filename,'w')
    ispis = narudzba.ispis()
    f.write(ispis) # python will convert \n to os.linesep
    f.close() # you can omit in most cases as the destructor will call it

    response = make_response(ispis)
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename)
    return response


@main.route('/narudzbe/brisi',  methods = ['POST'])
def brisi():
    narudzba=Narudzba.query.filter_by(narudzbaID = request.form.get('narudzbaID')).first()
    #treba poslati mail o ne prihvaćanju
    if not narudzba.potvrdjena:
        send_mail_to(narudzba.email, 'Narudžba nije prihvaćena zbog sumnje u ispravnost osobnih podataka')

    db.session.delete(narudzba)

    return prikaz_narudzbi()

@main.route('/narudzbe/prihvati',  methods = ['POST'])
def prihvati():
    narudzba=Narudzba.query.filter_by(narudzbaID = request.form.get('narudzbaID')).first()

    #i ovdje ćemo spremiti narudžbe i ime djelatnika koji ju je prihvatio da je možemo zatim izbrisati
    djelatnik = ucitaj_korisnika(current_user.get_id())
    narudzba.korisnici.append(djelatnik)
    current_user.brojNarudzbi+=1
    db.session.commit()
    if not narudzba.potvrdjena:
        narudzba.potvrdjena = True
          #treba poslati mail o prihvaćanju
        narudzba_ispis = narudzba.ispis()
        send_mail_to(narudzba.email, 'Narudžba je prihvaćena.' + '\n' + narudzba_ispis)

        vrijeme = datetime.now #zabilježimo vrijeme
        print(vrijeme)
        narudzbaStatistike = NarudzbaStatistika.query.filter_by(narudzbaID = request.form.get('narudzbaID'))
        
        narudzbaBroj = NarudzbaBroj (narudzbaCijenaDostave = narudzba.narudzbaCijenaDostave)
        db.session.add(narudzbaBroj)

        for stat in narudzbaStatistike:
            konstat = Statistika(
                jeloID = stat.jeloID,
                cijena = stat.cijena,
                #datetime = vrijeme
            )
            db.session.add(konstat)
      
    
    return prikaz_narudzbi()
   
    
@main.route('/statistika')
def statistika():
    triple = calcStats()
    promet = triple[0]
    avgPrice = triple[1]
    top3 = triple[2]
    return render_template('statistic.html', promet = promet, avgPrice = avgPrice, top3 = top3)


    
