from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, PasswordField, HiddenField
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
