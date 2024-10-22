'''
Sends an email with a verification link to the user
'''
from flask_mail import Mail, Message
from flask import url_for, render_template


mail = Mail()

def send_verification_email(user):

    token = user.generate_token()

    verification_url = url_for('/verify_email', token=token, _external=True)
    msg = Message(
            subject='Account verification',
            sender='eastmonarchkicks@gmail.com',
            recipients=[user.email]
            )
    msg.body = f'Click the following link to verify your email {verification_url}'
    msg.html = render_template('verification.html', user=user, verification_url=verification_url)
    mail.send(msg)
