'''
This module contains all models related to the app
'''
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()

class Users(db.Model):
    '''
    Defines the users table in the database
    It's attributes define the columns of the table
    The init method initializes the columns with data
    '''

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    agency = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, firstname, lastname, agency, email, password):
        '''
        Initializes the columns of the table with data
        '''
        self.firstname = firstname
        self.lastname = lastname
        self.agency = agency
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        '''
        Hashes the password and stores it in the database
        Password is hashed for security reasons
        '''
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        '''
        compares user password and stored hash to authenticate the user
        '''
        return check_password_hash(self.password, password)