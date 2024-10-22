'''
Run the application
Handles login management, creating initial admins and running the application
'''
from create_app import create_app
from model import db, bcrypt, Users
from utils.verfication import mail
from routes.authentication import auth


app = create_app()

''' 
initialize the instances with the app 
    so they can access configuration settings
'''
db.init_app(app)
bcrypt.init_app(app)
mail.init_app(app)

app.register_blueprint(auth)

with app.app_context():
    db.create_all()

create_models()

if __name__ == '__main__':
    app.run(debug=True)
