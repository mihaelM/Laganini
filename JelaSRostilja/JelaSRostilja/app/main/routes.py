from flask import render_template,redirect,url_for,request
from .forms import NameForm
from . import main
from .. import db
from ..models import User

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/users',methods=['GET','POST'])
def show_users():
    users=[]
    form=NameForm()
    
    if request.method=='POST':
        if form1.validate_on_submit():
            tmp=User()
            tmp.name=form1.name.data
            try:
                db.session.add(tmp)
            except:
                pass

    try:
        for i in db.session.query(User):
            users.append(i)
    except:
        pass
    return render_template('show_users.html',users=users,form=form)
