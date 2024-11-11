'''
this file contains routes that verify users and reverify them
'''
from flask import Blueprint, jsonify
from models import Users, db
from utils.resend import resend_verification_email


verify = Blueprint('verify', __name__)

@verify.route('verify_email/<token>')
def verify_email(token):
     
    user = Users.generate_token(token)

    if user:
        user.verified = True
        db.session.commit()
        return jsonify({'success': 'Email verified successfuly!'})
    else:
        return jsonify({'error': 'Verification failed, try again!'})

@verify.route('/resend_verification_email', methods=['POST'])
def resend_verification_email():

    data = request.json()
    email = data['email']

    user = Users.query.filter_by(email=email).first()

    if not user:
        return jsonfiy({'error': 'There is no account associated with this email!'})
    else:
        resend_verification_email(user)
        return jsonify({"error": "Please check your email for a verification link to complete the registration process!"})

