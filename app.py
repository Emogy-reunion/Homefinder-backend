'''
Run the application
Handles login management, creating initial admins and running the application
'''
from create_app import create_app
from model import db, bcrypt, Users, Properties, Images
from utils.verification import mail
from routes.authentication import auth
from routes.verification import verify
from routes.upload import post
from routes.reset_password import reset
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


app = create_app()

''' 
initialize the instances with the app 
    so they can access configuration settings
'''

jwt = JWTManager(app)
db.init_app(app)
bcrypt.init_app(app)
mail.init_app(app)


migrate = Migrate(app, db)

app.register_blueprint(auth)
app.register_blueprint(verify)
app.register_blueprint(reset)
app.register_blueprint(post)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
