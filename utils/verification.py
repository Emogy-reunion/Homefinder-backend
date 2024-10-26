'''
This file contains a function that sends verification emails
'''
from flask_mail import Mail, Message
from flask import url_for, render_template


mail = Mail()

def send_verification_email(user):

    token = user.generate_token()

    verification_url = url_for('/verify_email', token=token, _external=True)
    msg = Message(
            subject=Verify Email,
            sender='info.bytevision@gmail.com',
            recievers=[user.email]
            )
    msg.body = f"Click the following link to verify your email {verification_url}"
    msg.html = render_template('verification.html', verification_url=verification_url, username=user.firstname)
    mail.send(msg)
