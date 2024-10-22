'''
Initializes the application's forms
'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired, Regexp


class RegistrationForm(FlaskForm):
    '''
    Initializes the registration form fields
    Collects user data when creating an account
    '''

    firstname = StringField('First name', validators=[
        DataRequired(),
        Length(min=3, max=32, message='Name must be between 3 and 45 characters')
        ])
    lastname = StringField('Last name', validators=[
        DataRequired(),
        Length(min=3, max=32, message='Name must be between 3 and 45 characters')
        ])
    agency = StringField('Agency', validators=[
        DataRequired(),
        Length(min=3, max=32, message='Agency name must be between 3 and 45 characters')
        ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
        ])
    password = PasswordField('Password', validators=[
        Length(min=8, message="Password must be at least 8 characters long."),
        Regexp(r'(?=.*[A-Z])', message="Password must contain at least one uppercase letter."),
        Regexp(r'(?=.*[a-z])', message="Password must contain at least one lowercase letter."),
        Regexp(r'(?=.*\W)', message="Password must contain at least one special character.")
        ])
    confirmpassword = PasswordField('Confirm password', validators=[
        InputRequired(),
        EqualTo('password', message='Passwords must match!')
        ])
    showpassword = BooleanField('Show passwords')
    submit = SubmitField('Create Account')
