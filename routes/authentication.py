'''
This file contains routes that handle user authentication
'''
from flask import Blueprint, request, render_template, redirect, jsonify
from models import db, Users
from forms import RegistrationForm
from utils.verification import send_verification_email


auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    '''
    This routes allows users to create accounts
    It renders the form that collects the data
    It extractst the data and saves it to the database
    '''

    form = RegistrationForm()

    if request.method == 'POST':
        '''
        handles form submission
        '''

        if form.validate_on_submit():

            firstname = form.firstname.data
            lastname = form.lastname.data
            agency = form.agency.data
            email = form.email.data
            password = form.password.data

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
        else:
            return jsonify({'errors': form.errors})

    return render_template('register.html', form=form)

        
