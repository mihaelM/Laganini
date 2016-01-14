#!/usr/bin/python
# -*- coding: utf-8 -*-
from . import db, login_manager
from flask.ext.login import UserMixin, AnonymousUserMixin
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base



class Dozvole:
    KOMENTIRAJ = 0x01
    ODRADI_NARUDZBU = 0x02
    DODAJ_DJELATNIKA = 0x04
    ADMIN = 0x08


class Uloga(db.Model):
    __tablename__ = 'uloga'
    ulogaID = db.Column(db.Integer, primary_key=True)
    imeUloge = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    dozvole = db.Column(db.Integer)
    korisnici = db.relationship('Korisnik', backref='uloga', lazy='dynamic')

    @staticmethod
    def dodaj_uloge():
        uloge = {
            'Korisnik': (Dozvole.KOMENTIRAJ , True),
            'Djelatnik': (Dozvole.ODRADI_NARUDZBU , False),
            'Vlasnik': (Dozvole.ODRADI_NARUDZBU |
                        Dozvole.DODAJ_DJELATNIKA , False),
            'Administrator': (0xff, False)
        }
        for u in uloge:
            uloga = Uloga.query.filter_by(imeUloge=u).first()
            if uloga is None:
                uloga = Uloga(imeUloge=u)
            uloga.dozvole = uloge[u][0]
            uloga.default = uloge[u][1]
            db.session.add(uloga)
        db.session.commit()

    def __repr__(self):
        return '<Uloga: {}>'.format(self.imeUloge)

Korisnik_Potvrdi_Narudzba = db.Table('potvrdi', db.Model.metadata, #
        db.Column('korisnik_id', db.Integer, db.ForeignKey('korisnik.korisnikID') ),
        db.Column('narudzba_id', db.Integer, db.ForeignKey('narudzba.narudzbaID') )
)   


class Korisnik(UserMixin,db.Model):
    __tablename__='korisnik'
    korisnikID=db.Column(db.Integer,primary_key=True)
    korisnikKorisIme=db.Column(db.String(64))
    korisnikPas_hash=db.Column(db.String(128))
    ime=db.Column(db.String(64))
    prezime=db.Column(db.String(64))
    ulogaID=db.Column(db.Integer,db.ForeignKey('uloga.ulogaID'))
    komentari=db.relationship('Komentar',backref='korisnik',lazy='dynamic')
    ocjena=db.Column(db.Integer,default=0)

    narudzbe = db.relationship('Narudzba', secondary = Korisnik_Potvrdi_Narudzba, back_populates = 'korisnici') #djelatnici

    def get_id(self):
        return self.korisnikID

    def __init__(self,**kwargs):
        super(Korisnik,self).__init__(**kwargs)

    def __eq__(self, other):
        try:
            return self.korisnikID == other.korisnikID
        except Exception as e:
            return False


    def __repr__(self):
        return "<Korisnik: {}, korisnikID: {}>".format(self.korisnikKorisIme,self.korisnikID)
    
   
    @staticmethod
    def dodaj_admina(**kwargs):
        tmp=Korisnik(korisnikKorisIme="admin",ime="admin",prezime="admin",uloga=Uloga.query.filter_by(imeUloge="Administrator").first())
        tmp.korisnikPas="admin"
        try:
            db.session.add(tmp)
            db.session.commit()
        except:
            pass

    @property
    def korisnikPas(self):
        raise AttributeError('password je privatni atribut')

    @korisnikPas.setter
    def korisnikPas(self, password):
        self.korisnikPas_hash = generate_password_hash(password)

    def provjeri_password(self, password):
        return check_password_hash(self.korisnikPas_hash, password)

    def smije(self,dozvole):
        return self.uloga is not None and (self.uloga.dozvole & dozvole)==dozvole

class AnonimniKorisnik(AnonymousUserMixin):
    def smije(self, dozvole):
        return False

login_manager.anonymous_user=AnonimniKorisnik

@login_manager.user_loader
def ucitaj_korisnika(id):
    return Korisnik.query.get(int(id))

class Komentar(db.Model):
    __tablename__='komentar'
    klijentID=db.Column(db.Integer,db.ForeignKey('korisnik.korisnikID'))
    komentarID=db.Column(db.Integer,primary_key=True)
    tekstKomentara=db.Column(db.Unicode(1000))
    datum=db.Column(db.DateTime, index=True, default=datetime.now)

    def __init__(self,**kwargs):
        super(Komentar,self).__init__(**kwargs)

    def __repr__(self):
        return "<KomentarID: {}, : tekstKomentara: {}>".format(self.komentarID,self.tekstKomentara)


class Restoran(db.Model):
    __tablename__='restoran'
    restoranID=db.Column(db.Integer,primary_key=True)
    naziv=db.Column(db.Unicode(128))
    adresa=db.Column(db.Unicode(128))
    fotoID=db.Column(db.String(128))
    imeVlas=db.Column(db.Unicode(64))
    prezVlas=db.Column(db.Unicode(64))
    radnoVrijeme=db.Column(db.String(128))
    telefon=db.Column(db.String(128))
    minNarudzba=db.Column(db.Float)
    proVrijemeDost=db.Column(db.String(128))
    nacinPlac=db.Column(db.Unicode(128))
    cijenaDostave=db.Column(db.Float)
    evPopust=db.Column(db.Float) #hm da sto s tim

    def __repr__(self):
        return "<restoranID: {}, naziv: {}>".format(self.restoranID,self.naziv)

    @staticmethod
    def dodaj_restoran():
        tmp=Restoran(naziv="Wild8".decode('utf-8'),
                     adresa="Ulica Alena Bažanta 2".decode('utf-8'),
                     fotoID="slikaRestorana.jpg",
                     imeVlas="Ivica".decode('utf-8'),
                     prezVlas="Todorić".decode('utf-8'),
                     radnoVrijeme="8:00 - 23:00",
                     telefon="(01) 231 7463",
                     minNarudzba=100.0,
                     proVrijemeDost="40 min",
                     nacinPlac="Gotovinski ili kartično".decode('utf-8'),
                     cijenaDostave=5.0,
                     evPopust=0.0)
        try:
            db.session.add(tmp)
            db.session.commit()
        except:
            pass

    @staticmethod
    def izracunaj_ocjenu():
        suma=0
        br=0
        korisnici=Korisnik.query.filter_by(uloga=Uloga.query.filter_by(imeUloge='Korisnik').first()).all()
        for k in korisnici:
            if k.ocjena>0:
                suma+=k.ocjena
                br+=1
        if br==0:
            return -1
        else:
            return float(suma)/br

class Narudzba(db.Model):
    __tablename__='narudzba'
    narudzbaID=db.Column(db.Integer,primary_key=True, autoincrement = True)
    adresa=db.Column(db.String(128))
    kat=db.Column(db.Integer)
    kontakt_broj=db.Column(db.Integer)
    email=db.Column(db.String(128))
    placanje=db.Column(db.String(64))
    datum=db.Column(db.DateTime(), default=datetime.utcnow)
    opisNarudzbe = db.Column(db.Unicode(100000))
    narudzbaCijenaDostave = db.Column(db.Float) #novi podatak - ukupna cijena narudzbe
    cijenaHrane = db.Column(db.Float)
    potvrdjena = db.Column(db.Boolean, default = False)
   # jela = db.relationship ('Jelo', secondary = Jelo_Ima_Narudzba, back_populates = 'narudzbe')
    korisnici = db.relationship('Korisnik', secondary = Korisnik_Potvrdi_Narudzba, back_populates = 'narudzbe') #djelatnici

    def __init__(self,**kwargs):
        super(Narudzba,self).__init__(**kwargs)

    def __repr__(self):
        return "<NarudzbaID: {}, email: {}>".format(self.narudzbaID, self.email)

    def ispis(self):
        return " Adresa : {}\n Kat : {}\n Kontakt : {}\n Email: {}\n Placanje : {}\n Datum : {}\n Opis : {}\n Ukupna cijena : {}\n".format(
            self.adresa, self.kat, self.kontakt_broj, self.email, self.placanje, self.datum, self.opisNarudzbe, self.cijenaHrane+self.narudzbaCijenaDostave)

    def ispisKorisnici(self):
        s=""
        i = 0
        for korisnik in self.korisnici:
            if i == 0:
                s+=korisnik.korisnikKorisIme
                i+=1
            else:
                s+= " | " + korisnik.korisnikKorisIme
        return s



Jelo_Ima_Opcija = db.Table('ima', db.Model.metadata, #treba vidit za ovaj model.metadata
    db.Column('jelo_id', db.Integer, db.ForeignKey('jelo.jeloID')),
    db.Column('opcija_id', db.Integer, db.ForeignKey('opcija.opcijaID'))
 )


class Opcija(db.Model):
    __tablename__ = 'opcija'
    opcijaID = db.Column(db.Integer, primary_key = True)
    opcija = db.Column(db.Unicode(128))
    jela = db.relationship("Jelo", secondary = Jelo_Ima_Opcija, back_populates = "opcije")
    
    def __init__(self,**kwargs):
        super(Opcija,self).__init__(**kwargs)


class Jelo(db.Model):
    __tablename__ = 'jelo'
    jeloID = db.Column(db.Integer, primary_key = True)
    naziv = db.Column(db.Unicode(128))
    fotoJeloIme = db.Column(db.String(128))
    cijena = db.Column(db.Float)
    dostupnost = db.Column(db.Boolean)
    cestoNarucivano = db.Column (db.Boolean)
    kategorijaID = db.Column(db.Integer, db.ForeignKey('kategorija.kategorijaID')) #parentID
    #trebalo bi one foreign keyeve definirat ^^
    # narudzbe = db.relationship ('Narudzba', secondary = Jelo_Ima_Narudzba, back_populates = 'jela')
    opcije = db.relationship("Opcija", secondary=Jelo_Ima_Opcija, back_populates="jela")
     
    def __init__(self,**kwargs):
        super(Jelo,self).__init__(**kwargs)

   # tu fino mozemo definirat kako zelimo da izgleda na stranici :)
    def __repr__(self):
        return "{0:3d}. kategorija: {2}, naziv: {1} ".format( self.jeloID, self.naziv.encode('utf-8'),
        Kategorija.query.filter_by(kategorijaID=self.kategorijaID).first().kategorijaIme.encode('utf-8') )

# zasad stavljamo da ima tu jednu (ili nijednu) odabranu opciju, inače je prekomplicirano za nas neiskusne developere
class JeloKosarica(db.Model):
    __tablename__ = 'jelo_kosarica'
    jeloKosaricaID = db.Column (db.Integer, primary_key = True, autoincrement = True)
    jeloID = db.Column(db.Integer) #zapravo redundantno mozdaaa
    naziv = db.Column(db.Unicode(128))
    fotoJeloIme = db.Column(db.Unicode(128))
    cijena = db.Column(db.Float)
    dostupnost = db.Column(db.Boolean)
    cestoNarucivano = db.Column (db.Boolean)
    kategorijaID = db.Column(db.Integer, db.ForeignKey('kategorija.kategorijaID')) #parentID
    #trebalo bi one foreign keyeve definirat ^^
    opcija = db.Column(db.Unicode(128))
    kolicina = db.Column(db.Integer) # kolicina
    sessionID = db.Column(db.String(128))

    #djelatnicima nebitna cijena, ali neka im to da znaju sumirat
    def __repr__(self): #količina kolicina, zkj sad to ne radi???, broj porcija
        return "Naziv: {}, Cijena: {}kn , Količina: {}, Opcija: {}".format(self.naziv.encode('utf-8'),  self.cijena, self.kolicina,
                                                            'nema dodatne opcije' if self.opcija is None else self.opcija.encode('utf-8') )
    
    def __init__(self,**kwargs):
        super(JeloKosarica,self).__init__(**kwargs)
    
    def setKolicina (self, kolicina):
        self.kolicina = kolicina




class Kategorija(db.Model):
    __tablename__ = 'kategorija'
    kategorijaID = db.Column(db.Integer, primary_key = True)
    kategorijaIme = db.Column(db.Unicode(128))
    jela = db.relationship("Jelo", backref = 'kategorija', lazy = 'dynamic')

    def __init__(self,**kwargs):
        super(Kategorija,self).__init__(**kwargs)

    def __repr__(self):
        return "<KategorijaID: {}, KategorijaIme: {}>".format(self.kategorijaID,self.kategorijaIme)


    # 1-many with Narudzba, narudzba moze, mora biti foreign key
class NarudzbaStatistika(db.Model):
    narudzbaStatistikaID = db.Column(db.Integer, primary_key = True, autoincrement = True)
    narudzbaID=db.Column(db.Integer,db.ForeignKey('narudzba.narudzbaID'))
    cijena = db.Column(db.Float)
    jeloID = db.Column (db.Integer)
 
# s ovim se bavimo kad potvrdimo narudžbu, ok prenosio sam cijenu svakog jela
class Statistika(db.Model):
    __tablename__ = 'statistika'
    statistikaID = db.Column(db.Integer, primary_key = True, autoincrement = True)
    jeloID = db.Column(db.Integer)
    cijena = db.Column(db.Float) 
    datetime = db.Column(db.DateTime, index=True, default=datetime.utcnow) 

# također kad potvrdimo narudžbu
class NarudzbaBroj(db.Model):
    narudzbaBrojID = db.Column(db.Integer, primary_key = True, autoincrement = True)
    narudzbaCijenaDostave = db.Column(db.Float)
    datetime = db.Column(db.DateTime, index=True, default=datetime.utcnow) #podesimo mi kasnije vrijeme