from flask.ext.login import UserMixin
from . import db, login_manager
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash

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
            uloga.dozvola = uloge[u][0]
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



    def __init__(self,**kwargs):
        super(Korisnik,self).__init__(**kwargs)

    def __repr__(self):
        return "<Korisnik: {}, korisnikID: {}>".format(self.korisnikKorisIme,self.korisnikID)
    
    @staticmethod
    def dodajKorisnika(**kwargs):
        tmp=Korisnik(korisnikKorisIme=kwargs['username'],ime=kwargs['ime'],prezime=kwargs['prezime'])
        tmp.korisnikPas=kwargs['password']
        ## rjesiti uloge
        #tmp.ulogaID=
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
