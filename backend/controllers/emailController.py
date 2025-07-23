from flask_mail import Message
from extensions import mail

class EmailController:
    def __init__(self, mail):
        self.mail = mail

    @staticmethod
    def send_email(subject, recipients, body, html):
        msg = Message(subject, recipients=recipients, body=body, html=html)
        mail.send(msg)