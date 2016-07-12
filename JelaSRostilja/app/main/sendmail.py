# -*- coding: utf-8 -*-
import smtplib
from app import mail
from flask.ext.mail import Message
from flask import flash

def send_mail_to(s, mess):
     msg = Message("Pozdrav od WILD8",
                  sender="from@example.com",
                  recipients=[s])
     msg.body = mess
     try:
         mail.send(msg)
         flash('Poslan mail.')
     except Exception as e:
        flash('Korisnik je dao lažan mail.')