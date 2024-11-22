from flask import render_template, url_for
from flask_mail import Message
from utils.verification import mail

def reset_password_email(user):

    token = user.generate_token()
    verification_url = f"http://127.0.0.1:5000/reset-password?token={token}"
    msg = Message(
            subject='Password reset',
            sender='info.bytevision@gmail.com',
            recipients=[user.email]
            )
    msg.body = f'Click the following link to reset your password {verification_url}'

    try:
        msg.html = render_template('reset_password.html', name=user.firstname, verification_url=verification_url)
    except Exception as e:
        print(e)
    mail.send(msg)
