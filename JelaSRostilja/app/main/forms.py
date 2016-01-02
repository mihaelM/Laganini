from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, PasswordField, IntegerField
from wtforms.validators import DataRequired

class UnosKorisnika(Form):
    korisIme=StringField('Korisnicko ime', validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    ime=StringField('Ime',validators=[DataRequired()])
    prezime=StringField('Prezime',validators=[DataRequired()])
    uloga=SelectField('Uloga',choices=[('Korisnik','Korisnik'),('Djelatnik','Djelatnik'),('Administrator','Administrator')])
    submit=SubmitField('Dodaj')

class UnosKomentara(Form):
    tekst=StringField('Unesite komentar',validators=[DataRequired()])
    submit=SubmitField('Komentiraj')

class PodaciNarudzbe(Form):
    adresa = StringField('Adresa dostave (ulica i kućni broj)', validators = [DataRequired()])
    # ne mora biti logiran xD
    ime = StringField('Ime naručitelja', validators = [DataRequired()]) #ipak mislim da je ok da ovo piše
    prezime = StringField ('Prezime naručitelja', validators = [DataRequired()])
    kat = IntegerField ('Kat', validators = [DataRequired()])
    kontakt_broj_mob = StringField('Broj telefona/mobitela', validators = [DataRequired()])
    email = StringField('E - mail', validators = [DataRequired()])
    uloga=SelectField('Plaćanje',choices=[('Gotovinski','Gotovinski'), ('Kartično','Kartično')])
    submit=SubmitField('Konačna potvrda narudžbe')

    #datum se autogenerira
    #treba dodatno imati izgenerirati izbornik za izbor 'karticnog' ili 'gotovinskog' placanja ili
    #obavijest da se plaća isključivo gotovinski



   



