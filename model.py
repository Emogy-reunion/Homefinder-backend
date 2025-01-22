'''
This module contains all models related to the app
'''
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer
from create_app import create_app

app = create_app()
db = SQLAlchemy()
bcrypt = Bcrypt()
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

class Users(db.Model):
    '''
    Defines the users table in the database
    It's attributes define the columns of the table
    The init method initializes the columns with data
    Has a many to one relationship with the properties table
    '''

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    agency = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    verified = db.Column(db.Boolean, default=False)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    properties = db.relationship('Properties', back_populates='user', lazy=True)

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
        return bcrypt.check_password_hash(self.password, password)

    def generate_token(self):
        '''
        Generates the verification token
        '''
        return serializer.dumps({'user_id': self.id})

    @staticmethod
    def verify_token(token):
        try:
            data = serializer.loads(token, max_age=3600)
            return db.session.get(Users, data['user_id'])
        except Exception as e:
            return None


class Properties(db.Model):
    ''''
    table to store the property details
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    purpose = db.Column(db.String(30), nullable=False)
    latitude = db.Column(db.String(150), nullable=False)
    longitude = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    posted_at = db.Column(db.DateTime, default=datetime.utcnow())
    user = db.relationship('Users', back_populates='properties', lazy=True)
    images = db.relationship('Images', backref='property', lazy=True)

    def __init__(self, user_id, location, price, bedrooms, purpose,
                 latitude, longitude, description, status):

        self.user_id = user_id
        self.location = location
        self.price = price
        self.bedrooms = bedrooms
        self.purpose = purpose
        self.latitude = latitude
        self.longitude = longitude
        self.description = description
        self.status = status


class Images(db.Model):
    '''
    table to store the image properties
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    filename = db.Column(db.String(150), nullable=False)

    def __init__(self, property_id, filename):
        self.property_id = property_id
        self.filename = filename
