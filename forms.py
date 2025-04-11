'''
Defines classes that validate the applications form  input
'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, TextField, IntegerField, MultipleFileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, NumberRange, Optional

class RegistrationForm(FlaskForm):
    '''
    validates the registration form input
    '''
    firstname = StringField('First name', validators=[
        DataRequired(),
        Length(min=2, max=45, message='First name must be between 2 and 45 character long!')])
    lastname = StringField('Last name', validators=[
        DataRequired(),
        Length(min=2, max=45, message='Last name must be between 2 and 45 characters long!')])
    agency = StringField('Agency', validators=[
        DataRequired(),
        Length(min=2, max=45, message='Agency name must be between 2 and 45 characters long!')])
    Email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(min=2, max=45, message='Email must be between 6 and 45 letters!')])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long."),
        Regexp(r'(?=.*[A-Z])', message="Password must contain at least one uppercase letter."),
        Regexp(r'(?=.*[a-z])', message="Password must contain at least one lowercase letter."),
        Regexp(r'(?=.*\W)', message="Password must contain at least one special character.")
        ])
    confirmpassword = PasswordField('Confirm password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match!')])


class LoginForm(FlaskForm):
    '''
    validates the login form fields data
    '''
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(min=8, message="Password must be at least 8 characters long.")
        ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long.")])

class PropertyUploadForm(FlaskForm):
    '''
    validates the upload form data
    '''
    location = StringField('Location', validators=[
        DataRequired(),
        Length(min=3, max=45, message='Location must be between 3 and 45 characters long')
        ])
    price = FloatField('Price', validators=[
        DataRequired(),
        NumberRange(min=0, message='Price cannot be less than 0')])
    bedrooms = IntegerField('Bedrooms', validators=[
        DataRequired(),
        NumberRange(min=0, message='Bedrooms cannot be less than 0')])
    purpose = StringField('Purpose', validators=[
        DataRequired()])
    latitude = StringField('Latitude', validators=[
        DataRequired()])
    status = StingField('Status', validators=[
        DataRequired()])
    description = TextField('Description', validators=[
        DataRequired()])
    images = MultipleFileField('Images', validators=[
        DataRequired()])


class GuestSearchForm(FlaskForm):
    '''
    validates the logged out users search form input
    '''
    location = StringField('Location', validators=[
        Length(min=3, max=45, message='Location must be between 3 and 45 characters long')
        ])
    minimum_price = FloatField('Minimum price', validators=[
        NumberRange(min=0, message='Minimum price must not be less than 0!')])
    maximum_price = FloatField('Maximum price', validators=[
        NumberRange(min=0, message='Maximum price must not be less than 0!')])
    bedrooms = IntegerField('Bedrooms', validators=[
        NumberRange(min=0, message='Bedrooms cannot be less than 0')])
    status = StingField('Status')

class MemberSearchForm(FlaskForm):
    '''
    validates the logged in users search form input
    '''
    location = StringField('Location', validators=[
        Length(min=3, max=45, message='Location must be between 3 and 45 characters long')
        ])
    minimum_price = FloatField('Minimum price', validators=[
        NumberRange(min=0, message='Minimum price must not be less than 0!')])
    maximum_price = FloatField('Maximum price', validators=[
        NumberRange(min=0, message='Maximum price must not be less than 0!')])
    bedrooms = IntegerField('Bedrooms', validators=[
        NumberRange(min=0, message='Bedrooms cannot be less than 0')])
    status = StingField('Status')

class UpdatePropertyForm(FlaskForm):
    '''
    validates the update property form details
    '''
    location = StringField('Location', validators=[
        Optional(),
        Length(min=3, max=45, message='Location must be between 3 and 45 characters long')
        ])
    price = FloatField('Price', validators=[
        Optional(),
        NumberRange(min=0, message='Price cannot be less than 0')])
    bedrooms = IntegerField('Bedrooms', validators=[
        Optional(),
        NumberRange(min=0, message='Bedrooms cannot be less than 0')])
    purpose = StringField('Purpose', validators=[
        Optional()])
    latitude = StringField('Latitude', validators=[
        Optional()])
    status = StingField('Status', validators=[
        Optional()])
    description = TextField('Description', validators=[
        Optional(),
        Length(min=150, max=450, message='Description must be between 150 and 450 charcters long!])
