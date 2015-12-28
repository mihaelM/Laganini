from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired,Email

class PrijavaKorisnika(Form):
    username=StringField('Korisnicko ime',validators=[DataRequired()])
    password = PasswordField('Lozinka', validators=[DataRequired()])
    submit=SubmitField('Prijava')