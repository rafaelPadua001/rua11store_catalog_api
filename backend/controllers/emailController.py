from flask_mail import Message
from extensions import mail
import os
from dotenv import load_dotenv

load_dotenv()

class EmailController:
    def __init__(self, mail):
        self.mail = mail

    @staticmethod
    def send_email(subject, recipients, body, html):
        #Logo URl
        logo_url = os.getenv('LOGO_URL')

        #Header 
        header_html =  f"""
            <div style="text-align:center; margin-bottom:20px;">
                <img src="{logo_url}" alt="Rua11Store" style="max-width:200px; height:auto;">
            </div>
        """
        # Footer
        footer_html =  """
            <br><br>
            <hr style="border:none; border-top:1px solid #ddd; margin:20px 0;">
            <p style="font-size:12px; color:#555; text-align:center;">
                &copy; 2025 Rua11Store - Todos os direitos reservados.<br>
                Este é um e-mail automático, por favor não responda.
            </p>
        """

        #mount mail
        final_html = f"""
            {header_html}
            {html}
            {footer_html}
        """
        msg = Message(subject, recipients=recipients, body=body, html=final_html)
        mail.send(msg)