from flask_mail import Message


class EmailController:
    def __init__(self, mail):
        self.mail = mail

    def send_email(self, subject, recipients, body, html):
        msg = Message(subject, recipients=recipients, body=body, html=html)
        self.mail.send(msg)