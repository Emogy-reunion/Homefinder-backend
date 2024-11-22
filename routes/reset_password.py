from flask import Blueprint, request, jsonify
from model import db, Users
import re
from email_validator import validate_email, EmailNotValidError
from utils.password_reset_email import password_reset_email


reset = Blueprint('reset', __name__)

@reset.route('/forgot_password')
def forgot_password():
    '''
    Sends an email with token to the user to verify their identity
    '''
    email = request.json['email'].lower()

    errors = {}

    if not email:
        errors[email] = 'Email is required!'
    else:
        try:
            valid = validate_email(email)
        except EmailNotValidError as e:
            errors[email] = 'Invalid email format!'

    if errors:
        return jsonify({'errors': errors})

    user = Users.query.filter_by(email=email).first()
    if user:
        password_reset_email(user)
        return jsonify({'success': 'Password reset instructions sent to your email!'})
    else:
        return jsonify({'error': "Account doesn't exist!"})

@reset.route('/reset_password<int:id>', methods=['POST'])
def reset_password(id):
    '''
    saves the new passwords to the database
    '''
    password = request.json['password']

    user = db.session.get[Users, id]

    errors = {}
    if not password:
        errors['password'] = 'Password is required!'
    elif len(password) < 8:
        errors['password'] = 'Password must be at least 8 characters long!'
    elif not re.search(r"[A-Z]", password):
        errors['password'] = 'Password must contain at least one uppercase letter!'
    elif not re.search(r"[a-z]", password):
        errors['password'] = 'Password must contain at least one lowercase letter!'
    elif not re.search(r"[0-9]", password):
        errors['password'] = 'Password must contain at least one digit!'
    elif not re.search(r"[@$!%*?&]", password):
        errors['password'] = 'Password must contain at least one special character (@$!%*?&)!'

    if errors:
        return jsonify({'errors': errors})

    user.password = password
    return jsonify({'success': 'Password updated successfully!'})
