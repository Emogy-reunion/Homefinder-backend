'''
contains routes that fetch and display properties for logged out users
'''
from flask import Blueprint, jsonify, request
from model import db, Users, Properties, Images
from sqlalchemy.orm import selectinload


listings = Blueprint('listings', __name__)


@listings.route('/rent', methods=['GET'])
def rent():
    '''
    retrieves properties for rent from the database
    paginates them and returns them to the user
    '''
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    properties = Properties.query.filter_by(purpose='rent').options(selectinload(Properties.images))

   
    paginated_results = properties.paginate(page=page, per_page=per_page)

    rentals = []

    if not paginated_results.items:
        return jsonify({'error': 'Properties not found!'})
    else:
        for rental in paginated_results.items:
            rentals.append({
                    'id': rental.id,
                    'location': rental.location,
                    'bedrooms': rental.bedrooms,
                    'price': rental.price,
                    'image': [image.filename for image in rental.images[0]] if rental.images else []
                    })
        response = {
                'listings': rentals,
                'pagination': {
                    'total': paginated_results.total,
                    'next': paginated_results.next_num if paginated_results.has_next else None,
                    'prev': paginated_results.prev_num if paginated_results.has_prev else None,
                    'page': paginated_results.page,
                    'pages': paginated_results.pages,
                    'per_page': paginated_results.per_page
                    }
                }
        return jsonify(response)


@listings.route('/buy', methods=['GET'])
def buy():
    '''
    retrieves properties that are for sale from the database
    '''

    page = request.args.get('page', 1, type=float)
    per_page = request.args.get('per_page', 10, type=float)


    properties = Properties.query.filter_by(purpose='sale').options(selectinload(Properties.images))

    paginated_results = properties.paginate(page=page, per_page=per_page)
    listings = []

    if not paginated_results.items:
        return jsonify({'error': 'Property not found!'})
    else:
        for listing in paginated_results.items:
            listings.append({
                'id': listing.id,
                'location': listing.location,
                'bedrooms': listing.bedrooms,
                'price': listing.price,
                'image': [image.filename for image in listing.images[0]] if listing.images else []
                })
        response = {
                'listings': listings,
                'pagination': {
                    'total': paginated_results.total,
                    'next': paginated_results.next_num if paginated_results.has_next else None,
                    'prev': paginated_results.prev_num if paginated_results.has_prev else None,
                    'page': paginated_results.page,
                    'pages': paginated_results.pages,
                    'per_page': paginated_results.per_page
                    }
                }

@listings.route('/listing_details/<int: property_id>', methods=['GET'])
def listing_details(property_id):
    '''
    retrieves property details from the database
    '''

    listing = Properties.query.filter_by(id=property_id).first()

    if not listing:
        return jsonify({'error': 'Property not found!'})

    response = {
            'user_id': listing.user_id,
            'location': listing.location,
            'price': listing.price,
            'bedrooms': listing.bedrooms,
            'agency': listing.agency,
            'latitude': listing.latitude,
            'longitude': listing.longitude,
            'purpose': listing.purpose,
            'images': [image.filename for image in rental.images] if listing.images else []
            }
    return jsonify(response)



