'''
this file contains routes that verify users and reverify them
'''
from flask import Blueprint, jsonify
from models import Users, db


verify = Blueprint('verify', __name__)

@verify.route('verify_email/<token>')
def verify_email(token):
     
    user = Users.generate_token(token)

    if user:
        user.verified = True
        db.session.commit()
        return jsonify({'success': 'Email verified successfuly!'})
    else:
        return jsonify({'Error': 'Verification failed, try again'})
