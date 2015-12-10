from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(Form):
    korisIme=StringField('Enter a name', validators=[Required()])
    potrvrdi=SubmitField('Submit')
