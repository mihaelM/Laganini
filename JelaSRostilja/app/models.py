from flask.ext.login import UserMixin
from . import db, login_manager
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
    def umetni_uloge():
        uloge = {
            'Korisnik': (Dozvole.KOMENTIRAJ , True),
            'Djelatnik': (Dozvole.ODRADI_NARUDZBU , False),
            'Vlasnik': (Dozvole.ODRADI_NARUDZBU |
                        Dozvole.DODAJ_DJELATNIKA , False),
            'Administrator': (0xff, False)
        }
        # uf ovo je zeznuto desifrirat
        for u in uloge:
            uloga = Uloga.query.filter_by(imeUloge=u).first()
            if uloga is None: # sto napocetku je stavimo uloga = Ulaga (imeUloge je key = u), i ostalo postavimo poslije
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

    @property
    def korisnikPas(self):
        raise AttributeError('password je privatni atribut')

    @korisnikPas.setter
    def korisnikPas(self, password):
        self.korisnikPas_hash = generate_password_hash(password)

    def provjeri_password(self, password):
        return check_password_hash(self.korisnikPas_hash, password)

class Komentar(db.Model):
    __tablename__='komentar'
    klijentID=db.Column(db.Integer,db.ForeignKey('korisnik.korisnikID')) #ok nisam ja za komentare zadućen
    komentarID=db.Column(db.Integer,primary_key=True)
    tekstKomentara=db.Column(db.String(256))

    def __init__(self,**kwargs):
        super(Komentar,self).__init__(**kwargs)

    #Korisnik.query.filter_by(korisnikID=klijentID).first()
    def __repr__(self):
        return "Komentar: {} | korisnik = Pero Perić".format(self.tekstKomentara)

class Narudzba(db.Model):
    __tablename__='narudzba'
    narudzbaID=db.Column(db.Integer,primary_key=True)
    adresa=db.Column(db.String(128))
    kat=db.Column(db.Integer)
    kontakt_broj=db.Column(db.Integer)
    email=db.Column(db.String(128))
    placanje=db.Column(db.String(64))
    datum=db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self,**kwargs):
        super(Narudzba,self).__init__(**kwargs)

    def __repr__(self):
        return "<NarudzbaID: {}, email: {}>".format(self.narudzbaID, self.email)

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
    fotoJeloIme = db.Column(db.Unicode(128))
    cijena = db.Column(db.Float)
    dostupnost = db.Column(db.Boolean)
    cestoNarucivano = db.Column (db.Boolean)
    kategorijaID = db.Column(db.Integer, db.ForeignKey('kategorija.kategorijaID')) #parentID
    #trebalo bi one foreign keyeve definirat ^^
    opcije = db.relationship("Opcija", secondary=Jelo_Ima_Opcija, back_populates="jela")
     
    def __init__(self,**kwargs):
        super(Jelo,self).__init__(**kwargs)

   # tu fino mozemo definirat kako zelimo da izgleda na stranici :)
    def __repr__(self):
        return "{}, naziv: {} ".format(self.jeloID, self.naziv.encode('utf-8'))

# zasad stavljamo da ima tu jednu (ili nijednu) odabranu opciju, inače je prekomplicirano za nas neiskusne developere
class JeloKosarica(db.Model):
    __tablename__ = 'jelo_kosarica'
    jeloID = db.Column(db.Integer, primary_key = True)
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

    def __repr__(self):
        return "Naziv: {}, cijena: {}, kolicina: {}".format(self.naziv.encode('utf-8'), 
                                                                           self.cijena, self.kolicina)

    def __init__(self,**kwargs):
        super(JeloKosarica,self).__init__(**kwargs)




class Kategorija(db.Model):
    __tablename__ = 'kategorija'
    kategorijaID = db.Column(db.Integer, primary_key = True)
    kategorijaIme = db.Column(db.Unicode(128))
    jela = db.relationship("Jelo", backref = 'kategorija', lazy = 'dynamic')

    def __init__(self,**kwargs):
        super(Kategorija,self).__init__(**kwargs)

    def __repr__(self):
        return "<KategorijaID: {}, KategorijaIme: {}>".format(self.kategorijaID,self.kategorijaIme)

