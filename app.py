'''
Run the application
Handles login management, creating initial admins and running the application
'''
from create_app import create_app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
