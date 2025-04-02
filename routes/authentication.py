'''
This file contains routes that handle user authentication
'''
from flask import Blueprint, request, render_template, redirect, jsonify
from model import db, Users
from utils.verification import send_verification_email
from utils.validation import validate_firstname, validate_lastname, check_email
import re
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


    firstname = data.get('firstname').lower()
    lastname = data.get('lastname').lower()
    agency = data.get('agency').lower()
    email = data.get('email').lower()
    password = data.get('password')


    errors = {}

    firstname_errors = validate_firstname(firstname)
    lastname_errors = validate_lastname(lastname)
    email_errors = check_email(email)

    if firstname_errors:
        errors['firstname'] = firstname_errors

    if lastname_errors:
        errors['lastname'] = lastname_errors

    if email_errors:
        errors['email'] = email_errors

    if errors:
        return jsonify({'errors': errors}), 400

    user = None

    try:
        user = Users.query.filter_by(email=email).first()
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500

    if user:
        return jsonify({'error': 'An account associated with this email exists'}), 409
    else:
        try:
            new_user = Users(firstname=firstname, lastname=lastname, 
                             agency=agency, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500

        send_verification_email(new_user)
        return jsonify({'success': 'Your account has been successfully created. Please check your email for a verification link to complete the registration process.'}), 201


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

    email_errors = check_email(email)

    if email_errors:
        errors['email'] = email_errors


    if errors:
        return jsonify({'errors': errors}), 400

    user = None
    try:
        user = Users.query.filter_by(email=email).first()]
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500

    if not user:
        return jsonify({"error": "An account with this email doesn't exists!"}), 409
    else:
        if user.verified == True:
            if user.check_password(password):
                access_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id)

                response = jsonify({'success': 'Logged in successfully!'}), 200
                set_access_cookies(response, access_token)
                set_refresh_cookies(response, refresh_token)
                return response
            else:
                return jsonify({'error': 'Incorrect password. Please try again!'}), 409
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
    response = jsonify({'success': 'Logged out successfuly'})
    unset_jwt_cookies(response)
    return response

@auth.route('/protected', methods=['POST'])
@jwt_required()
def protected():
    '''
    route to that react uses to check if the user is logged in
    '''
    return jsonify({"success": 'User is logged in!'})
