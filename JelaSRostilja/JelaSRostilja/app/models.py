from flask.ext.login import UserMixin
from . import db, login_manager

class User(UserMixin,db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)

    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)

    def __repr__(self):
        return "<User: {}, Id: {}>".format(self.name,self.id)

    def add_user(name='default'):
        tmp=User()
        tmp.name=name
        try:
            db.session.add(tmp)
            db.session.commit()
        except:
            pass
