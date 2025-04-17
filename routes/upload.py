from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from model import db, Users, Properties, Images
from utils.allowed_file import allowed_file
from werkzeug.utils import secure_filename
from forms import PropertyUploadForm

post = Blueprint('post', __name__)


@post.route('/upload', methods=['POST'])
@jwt_required()
def upload():
    '''
    route to allow users to upload properties
    saves them to the database
    '''
    if not request.files:
        return jsonify({"error": 'Please select one or more images for the property!'}), 400

    form = ProperyUploadForm(data.request.form)

    if form.validate():
        location = form.location.data.lower()
        price = form.price.data
        bedrooms = form.bedrooms.data
        purpose = form.purpose.data
        latitude = form.latitude.data
        longitude = form.longitude.data
        description = form.description.data
        status = form.status.data
        images = form.images.data

        try:
            user_id = get_jwt_identity()
            new_property = Properties(user_id=user_id, location=location, price=price,
                                      bedrooms=bedrooms, purpose=purpose, latitude=latitude,
                                      longitude=longitude, description=description, status=status)
            db.session.add(new_property)
            db.session.flush()

            uploads = []
        
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
                    return jsonify({'error': 'Invalid file extension!'}), 400
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500
    
        if uploads:
            return jsonify({'success': 'Property uploaded successfully!'}), 201
        else:
            return jsonify({'error': 'Failed to upload property. Please try again!'}), 500
    else:
        return jsonify({'errors': form.errors}), 400
