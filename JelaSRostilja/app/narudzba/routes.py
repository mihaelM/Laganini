from flask import redirect, url_for

from . import narudzba

@narudzba.route('/kosarica',methods=['GET','POST'])
def kosarica():
    return redirect(url_for('main.index'))