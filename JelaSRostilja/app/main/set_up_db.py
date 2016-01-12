# -*- coding: utf-8 -*-
from .. import db
from ..models import *
from dodajKorisnike import *
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# (načelno) TREBA ZAKOMENTIRATI CIJELI SADRŽAJ CIJELE FUNKCIJE (NE I IME) FUNKCIJE init_insert_into_db(), AKO ŽELIMO DA NAM OSTANU PODATCI OD PROŠLOG POKRETANJA !!!
# ILI ODKOMENTIRATI AKO NE ŽELIMO
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
'''
ovako
recimo
'''

def init_insert_into_db():  
  #  db.reflect() #jer drop all nekad djelomicno faila
  
    db.drop_all()
    db.create_all()
    Uloga.dodaj_uloge()
    Korisnik.dodaj_admina()
    Restoran.dodaj_restoran()
    insert_korisnici()

    uloga_djelatnik = Uloga.query.filter_by(imeUloge = "Djelatnik").first()
    dodaj_korisnika("Dj_Ivo", "Ivo", "dj.i.", 'Ivić'.decode('utf-8'), uloga_djelatnik)

    kategorija1 = Kategorija (
        kategorijaID = 1, # db.Column(db.Integer, primary_key = True)
        kategorijaIme = 'dnevni meni' # db.Column(db.String(128))
    )
    kategorija2 = Kategorija (
        kategorijaID = 2, # db.Column(db.Integer, primary_key = True)
        kategorijaIme = 'kineska topla predjela' # db.Column(db.String(128))
    )
    kategorija3 = Kategorija (
        kategorijaID = 3, # db.Column(db.Integer, primary_key = True)
        kategorijaIme = 'pizze' # db.Column(db.String(128))
    )
    kategorija4 = Kategorija (
        kategorijaID = 4, # db.Column(db.Integer, primary_key = True)
        kategorijaIme = 'jela od mesa' # db.Column(db.String(128))
    )
    kategorija5 = Kategorija (
        kategorijaID = 5, # db.Column(db.Integer, primary_key = True)
        kategorijaIme = 'salate' # db.Column(db.String(128))
    )
    

    jelo1 = Jelo ( 
        jeloID = 1, # db.Column(db.Integer, primary_key = True)
        naziv = 'Hrskava patka s umakom (po izboru)', # db.Column(db.String(128)),
        fotoJeloIme = '1.jpg', # db.Column(db.String(128)) #mozda ovo ime
        cijena = 40, # db.Column(db.Float)
        dostupnost = True, # b.Column(db.Boolean)
        cestoNarucivano = True, # db.Column (db.Boolean)
        kategorijaID = 1  # db.Column(db.Integer, db.ForeignKey('kategorija.kategorijaID')) #parentID
        # opcije =  db.relationship("Opcija", secondary=Jelo_Ima_Opcija, back_populates="jela"), kasnije popunimo ju
    )
    jelo2 = Jelo ( 
        jeloID = 2, # db.Column(db.Integer, primary_key = True)
        naziv = 'Piletina s povrćem'.decode('utf-8'), # db.Column(db.String(128)),
        fotoJeloIme = '2.jpg', # db.Column(db.String(128)) #mozda ovo ime
        cijena = 35, # db.Column(db.Float)
        dostupnost = True, # b.Column(db.Boolean)
        cestoNarucivano = True, # db.Column (db.Boolean)
        kategorijaID = 1  # db.Column(db.Integer, db.ForeignKey('kategorija.kategorijaID')) #parentID
        # opcije =  db.relationship("Opcija", secondary=Jelo_Ima_Opcija, back_populates="jela"), kasnije popunimo ju
    )

    jelo3 = Jelo ( 
        jeloID = 3, # db.Column(db.Integer, primary_key = True)
        naziv = '3 vrste mesa s povrćem'.decode('utf-8'), # db.Column(db.String(128)),
        fotoJeloIme = '3.jpg', # db.Column(db.String(128)) #mozda ovo ime
        cijena = 30, # db.Column(db.Float)
        dostupnost = False, # b.Column(db.Boolean)
        cestoNarucivano = True, # db.Column (db.Boolean)
        kategorijaID = 1  # db.Column(db.Integer, db.ForeignKey('kategorija.kategorijaID')) #parentID
        # opcije =  db.relationship("Opcija", secondary=Jelo_Ima_Opcija, back_populates="jela"), kasnije popunimo ju
    )

    jelo4 = Jelo ( 
        jeloID = 4, # db.Column(db.Integer, primary_key = True)
        naziv = 'Japanski Yakitori', # db.Column(db.String(128)),
        fotoJeloIme = '4.jpg', # db.Column(db.String(128)) #mozda ovo ime
        cijena = 30, # db.Column(db.Float)
        dostupnost = True, # b.Column(db.Boolean)
        cestoNarucivano = True, # db.Column (db.Boolean)
        kategorijaID = 1  # db.Column(db.Integer, db.ForeignKey('kategorija.kategorijaID')) #parentID
        # opcije =  db.relationship("Opcija", secondary=Jelo_Ima_Opcija, back_populates="jela"), kasnije popunimo ju
    )
    jelo5 = Jelo ( 
        jeloID = 5, # db.Column(db.Integer, primary_key = True)
        naziv = 'Proljetne roladice s kozicama', # db.Column(db.String(128)),
        fotoJeloIme = '5.jpg', # db.Column(db.String(128)) #mozda ovo ime
        cijena = 21, # db.Column(db.Float)
        dostupnost = True, # b.Column(db.Boolean)
        cestoNarucivano = False, # db.Column (db.Boolean)
        kategorijaID = 2  # db.Column(db.Integer, db.ForeignKey('kategorija.kategorijaID')) #parentID
        # opcije =  db.relationship("Opcija", secondary=Jelo_Ima_Opcija, back_populates="jela"), kasnije popunimo ju
    )
    jelo6 = Jelo ( 
        jeloID = 6, # db.Column(db.Integer, primary_key = True)
        naziv = 'Vegeterijanske proljetne rolice', # db.Column(db.String(128)),
        fotoJeloIme = '6.jpg', # db.Column(db.String(128)) #mozda ovo ime
        cijena = 12, # db.Column(db.Float)
        dostupnost = False, # b.Column(db.Boolean)
        cestoNarucivano = False, # db.Column (db.Boolean)
        kategorijaID = 2  # db.Column(db.Integer, db.ForeignKey('kategorija.kategorijaID')) #parentID
        # opcije =  db.relationship("Opcija", secondary=Jelo_Ima_Opcija, back_populates="jela"), kasnije popunimo ju
    )
    jelo7 = Jelo ( 
        jeloID = 7, # db.Column(db.Integer, primary_key = True)
        naziv = 'Čips od jastoga & slatko-kiseli umak'.decode( 'utf-8' ), # db.Column(db.String(128)),
        fotoJeloIme = '7.jpg', # db.Column(db.String(128)) #mozda ovo ime
        cijena = 12, # db.Column(db.Float)
        dostupnost = False, # b.Column(db.Boolean)
        cestoNarucivano = False, # db.Column (db.Boolean)
        kategorijaID = 2  # db.Column(db.Integer, db.ForeignKey('kategorija.kategorijaID')) #parentID
        # opcije =  db.relationship("Opcija", secondary=Jelo_Ima_Opcija, back_populates="jela"), kasnije popunimo ju
    )

    jelo8 = Jelo ( 
        jeloID = 8, # db.Column(db.Integer, primary_key = True)
        naziv = 'Pohano povrće & slatko-kiseli umak'.decode('utf-8'), # db.Column(db.String(128)),
        fotoJeloIme = '8.jpg', # db.Column(db.String(128)) #mozda ovo ime
        cijena = 12, # db.Column(db.Float)
        dostupnost = True, # b.Column(db.Boolean)
        cestoNarucivano = False, # db.Column (db.Boolean)
        kategorijaID = 2  # db.Column(db.Integer, db.ForeignKey('kategorija.kategorijaID')) #parentID
        # opcije =  db.relationship("Opcija", secondary=Jelo_Ima_Opcija, back_populates="jela"), kasnije popunimo ju
    )

    jelo9 = Jelo ( 
        jeloID = 9, # db.Column(db.Integer, primary_key = True)
        naziv = 'Pizza Capriciosa', # db.Column(db.String(128)),
        fotoJeloIme = '9.jpg', # db.Column(db.String(128)) #mozda ovo ime
        cijena = 36, # db.Column(db.Float)
        dostupnost = True, # b.Column(db.Boolean)
        cestoNarucivano = True, # db.Column (db.Boolean)
        kategorijaID = 3  # db.Column(db.Integer, db.ForeignKey('kategorija.kategorijaID')) #parentID
        # opcije =  db.relationship("Opcija", secondary=Jelo_Ima_Opcija, back_populates="jela"), kasnije popunimo ju
    )
    jelo10 = Jelo ( 
        jeloID = 10, # db.Column(db.Integer, primary_key = True)
        naziv = 'Pizza Quattro Formaggi', # db.Column(db.String(128)),
        fotoJeloIme = '10.jpg', # db.Column(db.String(128)) #mozda ovo ime
        cijena = 38, # db.Column(db.Float)
        dostupnost = True, # b.Column(db.Boolean)
        cestoNarucivano = True, # db.Column (db.Boolean)
        kategorijaID = 3  # db.Column(db.Integer, db.ForeignKey('kategorija.kategorijaID')) #parentID
        # opcije =  db.relationship("Opcija", secondary=Jelo_Ima_Opcija, back_populates="jela"), kasnije popunimo ju
    )
    jelo11 = Jelo ( 
        jeloID = 11, # db.Column(db.Integer, primary_key = True)
        naziv = 'Pizza Picante', # db.Column(db.String(128)),
        fotoJeloIme = '11.jpg', # db.Column(db.String(128)) #mozda ovo ime
        cijena = 38, # db.Column(db.Float)
        dostupnost = False, # b.Column(db.Boolean)
        cestoNarucivano = False, # db.Column (db.Boolean)
        kategorijaID = 3  # db.Column(db.Integer, db.ForeignKey('kategorija.kategorijaID')) #parentID
        # opcije =  db.relationship("Opcija", secondary=Jelo_Ima_Opcija, back_populates="jela"), kasnije popunimo ju
    )
    jelo12 = Jelo ( 
        jeloID = 12, # db.Column(db.Integer, primary_key = True)
        naziv = 'Slavnoska pizza', # db.Column(db.String(128)),
        fotoJeloIme = '12.jpg', # db.Column(db.String(128)) #mozda ovo ime
        cijena = 40, # db.Column(db.Float)
        dostupnost = True, # b.Column(db.Boolean)
        cestoNarucivano = True, # db.Column (db.Boolean)
        kategorijaID = 3  # db.Column(db.Integer, db.ForeignKey('kategorija.kategorijaID')) #parentID
        # opcije =  db.relationship("Opcija", secondary=Jelo_Ima_Opcija, back_populates="jela"), kasnije popunimo ju
    )
    jelo13 = Jelo ( 
        jeloID = 13, # db.Column(db.Integer, primary_key = True)
        naziv = 'Gurmanska pizza', # db.Column(db.String(128)),
        fotoJeloIme = '13.jpg', # db.Column(db.String(128)) #mozda ovo ime
        cijena = 40, # db.Column(db.Float)
        dostupnost = False, # b.Column(db.Boolean)
        cestoNarucivano = False, # db.Column (db.Boolean)
        kategorijaID = 3 # db.Column(db.Integer, db.ForeignKey('kategorija.kategorijaID')) #parentID
        # opcije =  db.relationship("Opcija", secondary=Jelo_Ima_Opcija, back_populates="jela"), kasnije popunimo ju
    )
    jelo14 = Jelo ( 
        jeloID = 14, # db.Column(db.Integer, primary_key = True)
        naziv = 'Pljeskavica & prilozi', # db.Column(db.String(128)),
        fotoJeloIme = '14.jpg', # db.Column(db.String(128)) #mozda ovo ime
        cijena = 40, # db.Column(db.Float)
        dostupnost = True, # b.Column(db.Boolean)
        cestoNarucivano = True, # db.Column (db.Boolean)
        kategorijaID = 4 # db.Column(db.Integer, db.ForeignKey('kategorija.kategorijaID')) #parentID
        # opcije =  db.relationship("Opcija", secondary=Jelo_Ima_Opcija, back_populates="jela"), kasnije popunimo ju
    )
    jelo15 = Jelo ( 
        jeloID = 15, # db.Column(db.Integer, primary_key = True)
        naziv = 'Mali ćevapi & prilozi'.decode('utf-8'), # db.Column(db.String(128)),
        fotoJeloIme = '15.jpg', # db.Column(db.String(128)) #mozda ovo ime
        cijena = 32, # db.Column(db.Float)
        dostupnost = True, # b.Column(db.Boolean)
        cestoNarucivano = False, # db.Column (db.Boolean)
        kategorijaID = 4  # db.Column(db.Integer, db.ForeignKey('kategorija.kategorijaID')) #parentID
        # opcije =  db.relationship("Opcija", secondary=Jelo_Ima_Opcija, back_populates="jela"), kasnije popunimo ju
    )
    jelo16 = Jelo ( 
        jeloID = 16, # db.Column(db.Integer, primary_key = True)
        naziv = 'Veliki ćevapi & prilozi'.decode('utf-8'), # db.Column(db.String(128)),
        fotoJeloIme = '16.jpg', # db.Column(db.String(128)) #mozda ovo ime
        cijena = 42, # db.Column(db.Float)
        dostupnost = True, # b.Column(db.Boolean)
        cestoNarucivano = False, # db.Column (db.Boolean)
        kategorijaID = 4  # db.Column(db.Integer, db.ForeignKey('kategorija.kategorijaID')) #parentID
        # opcije =  db.relationship("Opcija", secondary=Jelo_Ima_Opcija, back_populates="jela"), kasnije popunimo ju
    )
    jelo17 = Jelo ( 
        jeloID = 17, # db.Column(db.Integer, primary_key = True)
        naziv = 'Bečki odrezak & prilozi'.decode('utf-8'), # db.Column(db.String(128)),
        fotoJeloIme = '17.jpg', # db.Column(db.String(128)) #mozda ovo ime
        cijena = 40, # db.Column(db.Float)
        dostupnost = True, # b.Column(db.Boolean)
        cestoNarucivano = False, # db.Column (db.Boolean)
        kategorijaID = 4  # db.Column(db.Integer, db.ForeignKey('kategorija.kategorijaID')) #parentID
        # opcije =  db.relationship("Opcija", secondary=Jelo_Ima_Opcija, back_populates="jela"), kasnije popunimo ju
    )

    jelo18 = Jelo ( 
        jeloID = 18, # db.Column(db.Integer, primary_key = True)
        naziv = 'Pohani pureći odrezak & prilozi'.decode('utf-8'), # db.Column(db.String(128)),
        fotoJeloIme = '18.jpg', # db.Column(db.String(128)) #mozda ovo ime
        cijena = 45, # db.Column(db.Float)
        dostupnost = True, # b.Column(db.Boolean)
        cestoNarucivano = False, # db.Column (db.Boolean)
        kategorijaID = 4  # db.Column(db.Integer, db.ForeignKey('kategorija.kategorijaID')) #parentID
        # opcije =  db.relationship("Opcija", secondary=Jelo_Ima_Opcija, back_populates="jela"), kasnije popunimo ju
    )
    
    jelo19 = Jelo ( 
        jeloID = 19, # db.Column(db.Integer, primary_key = True)
        naziv = 'Grah salata', # db.Column(db.String(128)),
        fotoJeloIme = '19.jpg', # db.Column(db.String(128)) #mozda ovo ime
        cijena = 16, # db.Column(db.Float)
        dostupnost = True, # b.Column(db.Boolean)
        cestoNarucivano = False, # db.Column (db.Boolean)
        kategorijaID = 5  # db.Column(db.Integer, db.ForeignKey('kategorija.kategorijaID')) #parentID
        # opcije =  db.relationship("Opcija", secondary=Jelo_Ima_Opcija, back_populates="jela"), kasnije popunimo ju
    )

    jelo20 = Jelo ( 
        jeloID = 20, # db.Column(db.Integer, primary_key = True)
        naziv = 'Sezonska salata', # db.Column(db.String(128)),
        fotoJeloIme = '20.jpg', # db.Column(db.String(128)) #mozda ovo ime
        cijena = 16, # db.Column(db.Float)
        dostupnost = False, # b.Column(db.Boolean)
        cestoNarucivano = False, # db.Column (db.Boolean)
        kategorijaID = 5  # db.Column(db.Integer, db.ForeignKey('kategorija.kategorijaID')) #parentID
        # opcije =  db.relationship("Opcija", secondary=Jelo_Ima_Opcija, back_populates="jela"), kasnije popunimo ju
    )

    
    opcija1 = Opcija (
        opcijaID = 1, #db.Column(db.Integer, primary_key = True)
        opcija = 'ketchup' #db.Column(db.String)
        # jela = b.relationship("Jelo", secondary = Jelo_Ima_Opcija, back_populates = "opcije"
       )
    
    opcija2 = Opcija (
        opcijaID = 2, #db.Column(db.Integer, primary_key = True)
        opcija = 'majoneza' #db.Column(db.String)
        # jela = b.relationship("Jelo", secondary = Jelo_Ima_Opcija, back_populates = "opcije"
       )
    
    opcija3 = Opcija (
        opcijaID = 3, #db.Column(db.Integer, primary_key = True)
        opcija = 'ajvar' #db.Column(db.String)
        # jela = b.relationship("Jelo", secondary = Jelo_Ima_Opcija, back_populates = "opcije"
       )
    
    opcija4 = Opcija (
        opcijaID = 4, #db.Column(db.Integer, primary_key = True)
        opcija = 'maslina' #db.Column(db.String)
        # jela = b.relationship("Jelo", secondary = Jelo_Ima_Opcija, back_populates = "opcije"
       )
    
    opcija5 = Opcija (
        opcijaID = 5, #db.Column(db.Integer, primary_key = True)
        opcija = 'umak od gljiva' #db.Column(db.String)
        # jela = b.relationship("Jelo", secondary = Jelo_Ima_Opcija, back_populates = "opcije"
       )

    opcija6 = Opcija (
        opcijaID = 6,
        opcija = 'umak od rajcice'
    )
    
    jelo1.opcije.append(opcija5)
    jelo1.opcije.append(opcija6)
    jelo9.opcije.append(opcija4)
    jelo10.opcije.append(opcija4)
    jelo11.opcije.append(opcija4)
    jelo12.opcije.append(opcija4)
    jelo13.opcije.append(opcija4)
    jelo14.opcije.append(opcija1)
    jelo14.opcije.append(opcija2)
    jelo14.opcije.append(opcija3)
    jelo15.opcije.append(opcija1)
    jelo15.opcije.append(opcija2)
    jelo15.opcije.append(opcija3)
    jelo16.opcije.append(opcija1)
    jelo16.opcije.append(opcija2)
    jelo16.opcije.append(opcija3)
    jelo17.opcije.append(opcija1)
    jelo17.opcije.append(opcija2)
    jelo17.opcije.append(opcija3)
    jelo18.opcije.append(opcija1)
    jelo18.opcije.append(opcija2)
    jelo18.opcije.append(opcija3)

    db.session.add(kategorija1)
    db.session.add(kategorija2)
    db.session.add(kategorija3)
    db.session.add(kategorija4)
    db.session.add(kategorija5)

    db.session.add(jelo1)
    db.session.add(jelo2)
    db.session.add(jelo3)
    db.session.add(jelo4)
    db.session.add(jelo5)
    db.session.add(jelo6)
    db.session.add(jelo7)
    db.session.add(jelo8)
    db.session.add(jelo9)
    db.session.add(jelo10)
    db.session.add(jelo11)
    db.session.add(jelo12)
    db.session.add(jelo13)
    db.session.add(jelo14)
    db.session.add(jelo15)
    db.session.add(jelo16)
    db.session.add(jelo17)
    db.session.add(jelo18)
    db.session.add(jelo19)
    db.session.add(jelo20)

    db.session.add(opcija1)
    db.session.add(opcija2)
    db.session.add(opcija3)
    db.session.add(opcija4)
    db.session.add(opcija5)
    db.session.add(opcija6)

    novaKategorija = Kategorija.query.filter_by(kategorijaID=1).first()
    print (novaKategorija.kategorijaIme)
 
