from flask import Blueprint, request, jsonify, make_response
from controllers.emailController import EmailController;
from flask import current_app

email_bp = Blueprint('email', __name__)

@email_bp.route('/send_test_email', methods=["POST"])
def send_test_email():
    data = request.get_json()
    subject = data.get("subject")
    recipients = data.get("recipients")
    body = data.get("body")
    html = data.get("html")

    controller = EmailController(current_app.extensions['mail'])
    controller.send_email(subject, recipients, body, html)

    return jsonify({"message": "E-mail enviado com sucesso!"}), 200
