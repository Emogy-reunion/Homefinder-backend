'''
This file contains routes that handle user authentication
'''
from flask import Blueprint, request, render_template, redirect, jsonify
from model import db, Users
from utils.verification import send_verification_email
import re
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, jwt_required, get_jwt_identity, unset_jwt_cookies
from forms import RegistrationForm, LoginForm

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    '''
    This routes allows users to create accounts
    It renders the form that collects the data
    It extractst the data and saves it to the database
    '''
    form = RegistrationForm(data=request.get_json())

    if form.validate():
        firstname = form.firstname.data.lower()
        lastname = form.lastname.data.lower()
        agency = form.agency.data.lower()
        email = form.email.data.lower()
        password = form.password.data

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
    else:
        return jsonify({'errors': form.errors}), 400


@auth.route('/login', methods=['POST'])
def login():
    '''
    authenticates the user
    creates an access token
    '''

    form = LoginForm(request.get_json)

    if form.validate():
        email = form.email.data
        password = form.password.data

        user = None
    
        try:
            user = Users.query.filter_by(email=email).first()
        except Exception as e:
            return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500

        if not user:
        return jsonify({"error": "An account with this email doesn't exists!"}), 409
        else:
            try:
                if user.verified == True:
                    if user.check_password(password):
                        access_token = create_access_token(identity=user.id)
                        refresh_token = create_refresh_token(identity=user.id)

                        response = jsonify({'success': 'Logged in successfully!'}), 200
                        set_access_cookies(response, access_token)
                        set_refresh_cookies(response, refresh_token)
                        return response, 200
                    else:
                        return jsonify({'error': 'Incorrect password. Please try again!'}), 409
                else:
                    return jsonify({'unverified': 'Your account in unverified. Verify before login!'}), 401
            except Exception as e:
                return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500
    else:
        return jsonify({'errors': form.errors}), 400

@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    '''
    creates a new access token using refresh token
    '''
    try:
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id)
        response = jsonify({'success': 'Successfully created access token'}), 201
        set_access_cookies(access_token)
        return response
    except Exception as e:
        return jsonify({"error": 'An unexpected error occured. Please try again!'}), 500

@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    '''
    destroys the access and refresh cookies logging the user out of the session
    '''
    try:
        response = jsonify({'success': 'Logged out successfuly'}), 200
        unset_jwt_cookies(response)
        return response
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again'}), 500

@auth.route('/protected', methods=['POST'])
@jwt_required()
def protected():
    '''
    route to that react uses to check if the user is logged in
    '''
    return jsonify({"success": 'User is logged in!'})
