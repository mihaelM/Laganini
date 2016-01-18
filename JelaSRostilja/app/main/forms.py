from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, PasswordField, HiddenField, RadioField, IntegerField, FloatField
from wtforms.validators import DataRequired,EqualTo, NumberRange, Email, Regexp, Optional

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

class UnosOcjene(Form):
    ocjena=SelectField( 'Unesite ocjenu:', choices=[(5,5),(4,4),(3,3),(2,2),(1,1)])
    submit=SubmitField('Ocijeni')

class KosaricaForm(Form):
    kolicina = IntegerField('Količina (broj između 1 i 10)', validators = [DataRequired(), NumberRange(min=1, max=10, message = 'Broj mora biti između 1 i 10')])
    submit = SubmitField('Promijenite količinu jela')

class JeloForm(Form):
    kolicina = IntegerField('Količina (broj između 1 i 10)', validators = [DataRequired(), NumberRange(min=1, max=10, message = 'Broj mora biti između 1 i 10')])
    submit = SubmitField('Potvrdite jelo')

class IzbrisiJelo(Form):
    submit = SubmitField('Izbrišite jelo')

class PotvrdiKosaricu(Form):
    submit = SubmitField('Potvrdite sadržaj košarice')

class DodajJelo(Form):
    kolicinaJela = IntegerField('Količina jela', validators = [DataRequired(), NumberRange(min=1, max=10, message = 'Broj mora biti između 1 i 10')])
    submit = SubmitField('Dodaj jelo')

class DjelatnikBrisi(Form):
    submit = SubmitField('Izbrišite narudžbu')

class DjelatnikPotvrdi(Form):
    submit =SubmitField('Potvrdite narudžbu')

class DjelatnikSnimi(Form):
    submit = SubmitField('Snimite narudžbu')

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
    evPopust=StringField('Popust',validators=[DataRequired()]) # default=0,choices=[(1,'Da'),(0,'Ne')]
    submit=SubmitField('Izmjeni')

class PodaciNarudzbe(Form):
    adresa = StringField('Adresa dostave (ulica i kućni broj)', validators = [DataRequired()])
    # ne mora biti logiran xD
    ime = StringField('Ime naručitelja', validators = [DataRequired()]) #ipak mislim da je ok da ovo piše
    prezime = StringField ('Prezime naručitelja', validators = [DataRequired()])
    kat = StringField ('Kat', validators = [DataRequired('Kat mora biti broj'),Regexp('^[0-9]*$',0,'Kat mora biti broj (stavite 0 za prizemlje)')])
    kontakt_broj_mob = StringField('Broj telefona/mobitela', validators = [DataRequired()])
    email = StringField('E - mail', validators = [DataRequired(), Email('Greska u e-mail adresi')])
    uloga=SelectField('Plaćanje',choices=[('Gotovinski','Gotovinski'), ('Kartično','Kartično')])
    submit=SubmitField('Konačna potvrda narudžbe')

    #datum se autogenerira
    #treba dodatno imati izgenerirati izbornik za izbor 'karticnog' ili 'gotovinskog' placanja ili
    #obavijest da se plaća isključivo gotovinski



   



