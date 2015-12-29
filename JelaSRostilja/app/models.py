from flask.ext.login import UserMixin,AnonymousUserMixin
from . import db, login_manager
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

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
    def umetni_uloge():
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

class Korisnik(UserMixin,db.Model):
    __tablename__='korisnik'
    korisnikID=db.Column(db.Integer,primary_key=True)
    korisnikKorisIme=db.Column(db.String(64))
    korisnikPas_hash=db.Column(db.String(128))
    ime=db.Column(db.String(64))
    prezime=db.Column(db.String(64))
    ulogaID=db.Column(db.Integer,db.ForeignKey('uloga.ulogaID'))
    komentari=db.relationship('Komentar',backref='korisnik',lazy='dynamic')

    def get_id(self):
        return self.korisnikID

    def __init__(self,**kwargs):
        super(Korisnik,self).__init__(**kwargs)

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
    tekstKomentara=db.Column(db.String(256))
    datum=db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self,**kwargs):
        super(Komentar,self).__init__(**kwargs)

    def __repr__(self):
        return "<KomentarID: {}, : tekstKomentara: {}>".format(self.komentarID,self.tekstKomentara)


class Jelo(db.Model):
    __tablename__='jelo'
    jeloID=db.Column(db.Integer,primary_key=True)
    naziv=db.Column(db.String(128))
    cijena=db.Column(db.Float)
    dostupnost=db.Column(db.Boolean)
    fofoJeloID=db.Column(db.Integer)
    cestoNarucivano=db.Column(db.Boolean)
    kategorijaID=db.Column(db.Integer)

    def __repr__(self):
        return "<jeloID: {}, naziv: {}>".format(self.jeloID,self.naziv)
    

class Kategorija(db.Model):
    __tablename__='kategorija'
    kategorijaID=db.Column(db.Integer,primary_key=True)
    kategorijaIme=db.Column(db.String(128))

    def __repr__(self):
        return "<KategorijaID: {}, KategorijaIme: {}>".format(self.kategorijaID,self.kategorijaIme)


class Narudzba(db.Model):
    __tablename__='narudzba'
    narudzbaID=db.Column(db.Integer,primary_key=True)
    adresa=db.Column(db.String(128))
    kat=db.Column(db.Integer)
    kontakt_broj=db.Column(db.Integer)
    email=db.Column(db.String(128))
    placanje=db.Column(db.String(64))
    datum=db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return "<NarudzbaID: {}, email: {}>".format(self.narudzbaID,self.email)


class Restoran(db.Model):
    __tablename__ = 'restoran'
    restoranID = db.Column(db.Integer, primary_key = True)
    naziv = db.Column(db.String(128))
    adresa = db.Column(db.String(128))
    fotoID = db.Column(db.Integer)
    imeVlas = db.Column(db.String(128))
    prezVlas = db.Column(db.String(128))
    radnoVrijeme = db.Column(db.String(128))
    telefon = db.Column(db.String(128))
    minNarudzba = db.Column(db.Integer)
    proVrijemeDost = db.Column(db.String(128))
    nacinPlac = db.Column(db.String(128))
    cijanaDostave = db.Column(db.Float)
    evPopust = db.Column(db.Boolean)

    def __repr__(self):
        return "<RestoranID: {}, naziv: {}>".format(self.restoranID, self.naziv)