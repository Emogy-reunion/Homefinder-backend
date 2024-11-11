'''
This file contains routes that handle user authentication
'''
from flask import Blueprint, request, render_template, redirect, jsonify
from model import db, Users
from utils.verification import send_verification_email


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

    firstname = data.get('firstname')
    lastname = data.get('lastname')
    agency = data.get('agency')
    email = data.get('email')
    password = data.get('password')

    if not firstname:
        errors['firstname'] = 'First name is required!'

    if not lastname:
        errors['lastname'] = 'Lastname is required!'

    if not email:
        errors['email'] = 'Email is required!'
    elif '@' not in email:
        errors['email'] = 'Invalid email format!'

    if not agency:
        errors['agency'] = 'Agency is required!'
        
    if not password:
        errors['password'] = 'Password is required!'
    elif password < 6:
        errors['password'] = 'Password must be at least 6 characters long!'

    if errors:
        return jsonify({'formerrors': errors})


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
