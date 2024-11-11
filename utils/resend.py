from flask import render_template, url_for
from flask_mail import Message
from utils.verification import mail

def resend_verification_email(user):

    token = user.generate_token()
    verification_url = url_for('verify.verify_email', token=token, _external=True)
    msg = Message(
            subject='Identity verification',
            sender='info.bytevision@gmail.com',
            recipients=[user.email]
            )
    msg.body = f'Click the following link to verify your identity {verification_url}'
    msg.html = render_template('reverification.html', name=user.firstname, verification_url=verification_url)
    mail.send(msg)
