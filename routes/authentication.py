'''
This file contains routes that handle user authentication
'''
from flask import Blueprint, request, render_template, redirect, jsonify
from model import db, Users
from utils.verification import send_verification_email
import re
from email_validator import validate_email, EmailNotValidError
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, jwt_required, get_jwt_identity, unset_jwt_cookies

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

                response = jsonify({'success': 'Logged in successfully!'})
                set_access_cookies(response, access_token)
                set_refresh_cookies(response, refresh_token)
                return response
            else:
                return jsonify({'error': 'Incorrect password. Please try again!'})
        else:
            return jsonify({'unverified': 'Your account in unverified. Verify before login'})

@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    '''
    creates a new access token using refresh token
    '''
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    response = jsonify({'success': 'Successfully created access token'})
    set_access_cookies(access_token)
    return response

@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    '''
    destroys the access and refresh cookies logging the user out of the session
    '''
    response = ({'success': 'Logged out successfuly'})
    unset_jwt_cookies(response)
    return response

@auth.route('/protected', methods=['POST'])
@jwt_required()
def protected():
    '''
    route to that react uses to check if the user is logged in
    '''
    return jsonify({"success": 'User is logged in!'})
