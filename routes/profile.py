'''
contains routes that work on user profiles: display, update and delete profiles
'''
from flask import Blueprint, jsonify
from model import db, User
from flask_jwt_extended import get_jwt_identity, jwt_required

profile = Blueprint('profile', __name__)

@profile.route('/member_profile', methods=['GET'])
@jwt_required
def member_profile():
    '''
    retrieves the logged in user profiles
    '''
    user_id = get_jwt_identity()

    try:
        user = db.session.get(User, user_id)

        if not user:
            return jsonify({'error': 'User not found!'})
        response = jsonify({
            'firstname': user.firstname,
            'lastname': user.lastname,
            'agency': user.agency,
            'email': user.email
            }), 200
        return response
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured!'})
