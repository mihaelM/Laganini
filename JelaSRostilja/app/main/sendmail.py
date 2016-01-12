import smtplib
from app import mail
from flask.ext.mail import Message

def send_mail_to(s, mess):
     msg = Message("Pozdrav od WILD8",
                  sender="from@example.com",
                  recipients=[s])
     msg.body = mess
     try:
         mail.send(msg)
     except Exception as e:
         pass