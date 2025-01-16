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
from routes.search import find
from routes.reset_password import reset
from routes.guest_properties import listings
from routes.uploads import posts
from routes.profile import profile
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
app.register_blueprint(posts)
app.register_blueprint(profile)
app.register_blueprint(find)
<<<<<<< HEAD

=======
>>>>>>> feature/factory

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
