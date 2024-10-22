'''
Stores the applications configuration settings
'''
from dotenv import load_dotenv
import os


# loads the environment variables
load_dotenv()

class Config():
    '''
    creates the configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    MAIL_SERVER = 'smtp@gmail.com'
    MAIL_PORT = 587
    MAIL_USER_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = "eastmonarchkicks@gmail.com",
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
