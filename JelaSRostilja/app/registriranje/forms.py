from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email

class UnosKorisnika(Form):
    korisIme=StringField('Korisnicko ime', validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    ime=StringField('Ime',validators=[DataRequired()])
    prezime=StringField('Prezime',validators=[DataRequired()])
    uloga=SelectField('Uloga',choices=[('Korisnik','Korisnik'),('Djelatnik','Djelatnik'),('Administrator','Administrator')])
    submit=SubmitField('Dodaj')