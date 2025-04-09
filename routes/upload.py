from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from model import db, Users, Properties, Images
from utils.allowed_file import allowed_file
from werkzeug.utils import secure_filename

post = Blueprint('post', __name__)



@post.route('/upload', methods=['POST'])
@jwt_required()
def upload():
    '''
    route to allow users to upload properties
    saves them to the database
    '''
    user_id = get_jwt_identity()

    location = request.form.get('location')
    price = request.form.get('price')
    bedrooms = request.form.get('bedrooms')
    purpose = request.form.get('purpose')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    description = request.form.get('description')
    status = request.form.get('status')

    try:
        new_property = Properties(user_id=user_id, location=location, price=price,
                                  bedrooms=bedrooms, purpose=purpose, latitude=latitude,
                                  longitude=longitude, description=description, status=status)
        db.session.add(new_property)
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error ocurred. Please try again!'})

    db.session.commit()

    uploads = []
    try:
        for image in images:
            if image and allowed_file(image.filename):
                '''
                checks if the file exists and has a valid filename
                '''
                filename = secure_filename(image.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                uploads.append(filename)
                new_image = Images(property_id=new_property.id, filename=filename)
                db.session.add(new_image)
            else:
                return jsonify({'error': 'Invalid file extension!'})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to upload. Please try again'})
    return jsonify({'error': 'Property uploaded successfully!'})
