from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired,Email,EqualTo

class PrijavaKorisnika(Form):
    username=StringField('Korisnicko ime',validators=[DataRequired()])
    password = PasswordField('Lozinka', validators=[DataRequired()])
    submit=SubmitField('Prijava')

class RegistracijaKorisnika(Form):
    korisIme=StringField('Korisnicko ime', validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired(),EqualTo('password2', message='Passwordi nisu jednaki')])
    password2=PasswordField('Potvrdi password',validators=[DataRequired()])
    ime=StringField('Ime',validators=[DataRequired()])
    prezime=StringField('Prezime',validators=[DataRequired()])
    submit=SubmitField('Registriraj se')