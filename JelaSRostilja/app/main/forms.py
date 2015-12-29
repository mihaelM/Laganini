from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired

class UnosDjelatnika(Form):
    korisIme=StringField('Korisnicko ime', validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    ime=StringField('Ime',validators=[DataRequired()])
    prezime=StringField('Prezime',validators=[DataRequired()])
    submit=SubmitField('Dodaj')

class UnosKomentara(Form):
    tekst=StringField('Unesite komentar',validators=[DataRequired()])
    submit=SubmitField('Komentiraj')