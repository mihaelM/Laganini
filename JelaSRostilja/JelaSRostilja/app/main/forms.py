from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import Required

class UnosKorisnika(Form):
    korisIme=StringField('Korisnicko ime', validators=[Required()])
    password=PasswordField('Password',validators=[Required()])
    ime=StringField('Ime',validators=[Required()])
    prezime=StringField('Prezime',validators=[Required()])
    uloga=SelectField('Uloga',choices=[('0','Korisnik'),('1','Djelatnik'),('2','Administrator')])
    submit=SubmitField('Dodaj')
