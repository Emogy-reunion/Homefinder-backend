'''
This file contains routes that handle user authentication
'''
from flask import Blueprint, request, render_template, redirect, jsonify
from model import db, Users
from utils.verification import send_verification_email
import re
from email_validator import validate_email, EmailNotValidError
from flask_jwt_extended import create_access_token, create_refresh_token

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    '''
    This routes allows users to create accounts
    It renders the form that collects the data
    It extractst the data and saves it to the database
    '''
    data = request.json
    errors = {}

    firstname = data.get('firstname').lower()
    lastname = data.get('lastname').lower()
    agency = data.get('agency').lower()
    email = data.get('email').lower()
    password = data.get('password')

    if not firstname:
        errors['firstname'] = 'First name is required!'

    if not lastname:
        errors['lastname'] = 'Lastname is required!'

    if not email:
        errors['email'] = 'Email is required!'
    else:
        try:
            valid = validate_email(email)
        except EmailNotValidError as e:
            errors['email'] = str(e)

    if not agency:
        errors['agency'] = 'Agency is required!'
        
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


    user = Users.query.filter_by(email=email).first()

    if user:
        return jsonify({'error': 'An account associated with this email exists'})
    else:
        try:
            new_user = Users(firstname=firstname, lastname=lastname, 
                             agency=agency, email=email, password=password)
            db.session.add(new_user)
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'An unexpected error occured. Try again!'})
        db.session.commit()

        send_verification_email(new_user)
        return jsonify({'success': 'Your account has been successfully created. Please check your email for a verification link to complete the registration process.'})


@auth.route('/login', methods=['POST'])
def login():
    '''
    authenticates the user
    creates an access token
    '''
    data = request.json
    email = data.get('email').lower()
    password = data.get('password')

    errors = {}

    if not email:
        errors[email] = 'Email is required!'
    else:
        try:
            valid = validate_email(email)
        except EmailNotValidError as e:
            errors['email'] = 'Invalid email format!'

    if not password:
        errors['password'] = 'Password is required!'

    if errors:
        return jsonify({'errors': errors})

    user = Users.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Account with this email doesn't exist"})
    else:
        if user.verified == True:
            if user.check_password(password):
                access_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id)

                return jsonify(access_token=access_token, refresh_token=refresh_token)
            else:
                return jsonify({'error': 'Incorrect password. Please try again!'})
        else:
            return jsonify({'unverified': 'Your account in unverified. Verify before login'})


