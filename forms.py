'''
Defines classes that validate the applications form  input
'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    '''
    validates the registration form input
    '''
    firstname = StringField('First name', validators=[
        DataRequired(),
        Length(min=2, max=45, message='First name must be between 2 and 45 letters!')])
    lastname = StringField('Last name', validators=[
        DataRequired(),
        Length(min=2, max=45, message='Last name must be between 2 and 45 letters!')])
    agency = StringField('Agency', validators=[
        DataRequired(),
        Length(min=2, max=45, message='Agency name must be between 2 and 45 letters!')])
    Email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(min=2, max=45, message='Email must be between 6 and 45 letters!')])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Regexp(r'(?=.*[A-Z])', message="Password must contain at least one uppercase letter."),
        Regexp(r'(?=.*[a-z])', message="Password must contain at least one lowercase letter."),
        Regexp(r'(?=.*\W)', message="Password must contain at least one special character.")
        ])
    confirmpassword = PasswordField('Confirm password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match!')])


