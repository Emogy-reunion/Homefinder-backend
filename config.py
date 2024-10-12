'''
Stores the applications configuration settings
'''
from dotenv import load_dotenv


# loads the environment variables
load_dotenv()

class Config():
    '''
    creates the configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
