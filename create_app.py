'''
This is an app factory
'''
from flask import Flask
from config import Config


def create_app():
    '''
    Creates the flask application instance
    It initializes the app's configuration settings
    It returns the application instance
    '''

    app = Flask(__name__)
    app.config.from_object(Config)
    return app
