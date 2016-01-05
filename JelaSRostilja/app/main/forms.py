from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, PasswordField, HiddenField, RadioField, IntegerField
from wtforms.validators import DataRequired,EqualTo

class UnosDjelatnika(Form):
    korisIme=StringField('Korisnicko ime', validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired(),EqualTo('password2', message='Passwordi nisu jednaki')])
    password2=PasswordField('Potvrdi password',validators=[DataRequired()])
    ime=StringField('Ime',validators=[DataRequired()])
    prezime=StringField('Prezime',validators=[DataRequired()])
    submit=SubmitField('Dodaj')

class UnosKomentara(Form):
    tekst=StringField('Unesite komentar',validators=[DataRequired()])
    submit=SubmitField('Komentiraj')

class ObrisiDjelatnika(Form):
    id=HiddenField('id',validators=[DataRequired()])
    submit=SubmitField('Obrisi')

class IzmjeniPodatkeRestorana(Form):
    naziv=StringField('Naziv',validators=[DataRequired()])
    adresa=StringField('Adresa',validators=[DataRequired()])
    imeVlas=StringField('Ime vlasnika',validators=[DataRequired()])
    prezVlas=StringField('Prezime vlasnika',validators=[DataRequired()])
    radnoVrijeme=StringField('Radno vrijeme',validators=[DataRequired()])
    telefon=StringField('Telefon',validators=[DataRequired()])
    minNarudzba=StringField('Minimalna narudzba',validators=[DataRequired()])
    proVrijemeDost=StringField('Prosjecno vrijeme dostave',validators=[DataRequired()])
    nacinPlac=StringField('Nacnin placanja',validators=[DataRequired()])
    cijenaDostave=StringField('Cijena dostave',validators=[DataRequired()])
    evPopust=RadioField('Popust',default=0,choices=[(1,'Da'),(0,'Ne')],validators=[DataRequired()])
    submit=SubmitField('Izmjeni')

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



   



