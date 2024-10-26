'''
Run the application
Handles login management, creating initial admins and running the application
'''
from create_app import create_app
from model import db, bcrypt, Users
from utils.verification import mail
from routes.authentication import auth
from flask_migrate import Migrate


app = create_app()

''' 
initialize the instances with the app 
    so they can access configuration settings
'''
db.init_app(app)
bcrypt.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(auth)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
