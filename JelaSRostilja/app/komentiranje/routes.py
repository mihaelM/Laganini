from flask import render_template, redirect, url_for, request, flash
from . forms import UnosKomentara
from . import komentiranje
from .. import db
from .. models import Komentar

@komentiranje.route('/komentari',methods=['GET','POST'])
def komentari():
    form=UnosKomentara()   
    if request.method=='POST':
        if form.validate_on_submit():
            komentar=Komentar(tekstKomentara=form.tekst.data)
            db.session.add(komentar)

            flash('Komentar spjesno objavljen')
            return redirect(url_for('komentiranje.komentari'))
    else:
        query = Komentar.query
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Komentar.komentarID.desc()).paginate(page, per_page=100,error_out=False)
    komentari = pagination.items
    return render_template('komentiranje/komentari.html',form=form,pagination=pagination,komentari=komentari)