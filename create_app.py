'''
This is an app factory
'''
from flask import Flask


def create_app():
    '''
    Creates the flask application instance
    It initializes the app's configuration settings
    It returns the application instance
    '''

    app = Flask(__name__)
    return app
