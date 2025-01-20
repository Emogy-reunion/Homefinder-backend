'''
Holds routes that conduct property searches
'''
from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from model import db, Users, Images, Properties
from sqlalchemy.orm import selectinload


find = Blueprint('find', __name__)

@find.route('/member_search', methods=['GET'])
@jwt_required()
def member_search():
    '''
    allows logged in users to filter products they have posted
    '''
    user_id = get_jwt_identity()
    location = request.args.get('location')
    minimum_price = request.args.get('minimum_price', type=float)
    maximum_price = request.args.get('maximum_price', type=float)
    bedrooms = request.args.get('bedrooms', type=int)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10)

    properties = Properties.query.filter_by(user_id=user_id)

    if location is not None:
        properties = properties.filter(Properties.location.ilike(f"%{location}%"))
    
    if minimum_price is not None:
        properties = properties.filter(Properties.price >= minimum_price)

    if maximum_price is not None:
        properties = properties.filter(Properties.price <= maximum_price)

    if bedrooms is not None:
        bedrooms = properties.filter(Properties.bedrooms == bedrooms)


    properties = properties.query.options(selectinload(Properties.images))
    paginated_results = properties.paginate(page=page, per_page=per_page)

    property_listings = []

    if not paginated_results.items:
        return jsonify({'error': 'Properties not available!'})
    else:
        for listing in paginated_results.items:
            property_listings.append({
                'id': listing.id,
                'location': listing.location,
                'price': listing.price,
                'bedrooms': listing.bedrooms,
                'image': [image.filename for image in listing.images[0]] if images else []
                })

        response = {
                'properties': property_listings,
                'pagination': {
                    'total': paginated_results.total,
                    'page': paginated_results.page,
                    'per_page': paginated_results.per_page,
                    'prev': paginated_results.prev_num if paginated_results.has_prev else None,
                    'next': paginated_results.next_num if paginated_results.has else None
                    }
                }
        return jsonify(response)

@find.route('/guest_search', methods=['GET'])
def guest_search():
    '''
    allows logged out users to filter products
    '''
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    location = request.args.get('location')
    bedrooms = request.args.get('bedrooms', type=int)
    minimum_price = request.args.get('minimum_price', type=float)
    maximum_price = request.args.get('maximum_price', type=float)

    properties = Properties.query

    if location is not None:
        properties = properties.filter(Properties.location.ilike(f"%{location}%"))

    if minimum_price is not None:
        properties = properties.filter(Properties.price >= minimum_price)

    if maximum_price is not None:
        properties = properties.filter(Properties.price <= maximum_price)

    if bedrooms is not None:
        properties = properties.filter(Properties.bedrooms == bedrooms)

    properties = properties.query.options(selectinload(Properties.images))
    paginated_results = properties.paginate(page=page, per_page=per_page)

    listings = []
    if not paginated_results.items:
        return jsonify({'error': 'Property not available!'})
    else:
        for listing in paginated_results.items:
            listings.append({
                'id': listing.id,
                'bedrooms': listing.bedrooms,
                'price': listing.price,
                'location': listing.location,
                'image': [image.filename for image in listing.images[0]] if listing.images else []
                })
    response = {
            'listings': listings,
            'pagination': {
                'total': paginated_results.items,
                'page': paginated_results.page,
                'per_page': paginated_results.per_page,
                'next': paginated_results.next_num if paginated_results.has_next else None,
                'prev': paginated_results.prev_num if paginated_results.has_prev else None
                }
            }
    return jsonify(response)


