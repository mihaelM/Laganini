from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class UnosKomentara(Form):
    tekst=StringField('Unesite komentar',validators=[DataRequired()])
    submit=SubmitField('Komentiraj')