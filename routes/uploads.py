from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from model import db, Users, Images, Properties
from sqlalchemy.orm import selectinload
from forms import UpdatePropertyForm


posts = Blueprint('posts', __name__)


@posts.route('/member_property_preview', methods=['GET'])
@jwt_required()
def member_property_preview():
    '''
    loads posts posted by a specific user
    returns the post and pagination details
    '''

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)

    try:
        user_id = get_jwt_identity()
        listings = Properties.query.filter_by(user_id=user_id).options(selectinload(Properties.images))
        paginated_results = listings.paginate(page=page, per_page=per_page)
    
        properties = []

        if not paginated_results.items:
            return jsonify({'error': 'Property not found!'}), 404
        else:
            for item in paginated_results.items:
                properties.append({
                    'id': item.id,
                    'location': item.location,
                    'price': item.price,
                    'bedrooms': item.bedrooms,
                    'status': item.status,
                    'image': [image.filename for image in item.images[0]] if images else []
                    })

            response = {
                    'properties': properties,
                    'pagination': {
                        "total": paginated_results.total,
                        "page": paginated_results.page,
                        "pages": paginated_results.pages,
                        "per_page": paginated_results.per_page,
                        "next": paginated_results.next_num if paginated_results.has_next else None,
                        "prev": paginated_results.prev_num if paginated_results.has_prev else None
                        }
                    }
            return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500

@posts.route('/member_property_details/<int:property_id>', methods=['GET'])
@jwt_required()
def member_property_details(property_id):
    '''
    Retrieves an item's details e.g map, description, images e.t.c
    '''
    try:
        details = Properties.query.filter_by(id=property_id).options(selectionload(Properties.images)).first()

        if not details:
            return jsonify({'error': 'Property not found'}), 404

        property_details = {
                'id': details.id,
                'location': details.location,
                'price': details.price,
                'bedrooms': details.bedrooms,
                'purpose': details.purpose,
                'latitude': details.latitude,
                'longitude': details.longitude,
                'description': details.description,
                'status': details.status,
                'images': [image.filename for image in details.images] if images else []
                }
        return jsonify(property_details)
    except Exception as e:
        return jsonify('error': 'An unexpected error occured. Please try again!'})


@posts.route('/update_property/<int:property_id>', methods=['PATCH'])
@jwt_required()
def update_property(property_id):
    '''
    allows logged in users to update their posts
    '''

    form = UpdatePropertyForm(request.get_json)
    if not form.validate():
        return jsonify({'errors': form.errors}), 400
    data = request.json

    location = form.location.data
    price = form.price.data
    bedrooms = form.bedrooms.data
    purpose = form.purpose.data
    latitude = form.latitude.data
    longitude = form.longitude.data
    description = form.description.data
    status = form.status.data

    try:
        property_listing = Properties.query(id=property_id).first()

        if not property_listing:
            return jsonify({'error': 'Property not found!'}), 404

        if location:
            property_listing.location = location

        if price:
            property_listing.price = price

        if bedrooms:
            property_listing.bedrooms = bedrooms

        if purpose:
            property_listing.purpose = purpose

        if latitude:
            property_listing.latitude = latitude

        if longitude:
            property_listing.longitude = longitude

        if description:
            property_listing.description = description

        if status:
            property_listing.status = status

        db.session.add(property_listing)
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500

    db.session.commit()
    return jsonify({'success': 'Property updated successfully!'}), 200


@posts.route('/delete_property<int:property_id>', methods=['DELETE'])
@jwt_required()
def delete_property(property_id):
    '''
    deletes a specific property listing from the database
    '''

    try:
        property_listing = Properties.query(id=property_id).first()

        if not property_listing:
            return jsonify({'error': 'Property not found!'}), 404
        
        db.session.delete(property_listing)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500
    return jsonify({'success': 'Property deleted successfully!'}), 200
