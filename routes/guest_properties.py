'''
contains routes that fetch and display properties for logged out users
'''
from flask import Blueprint, jsonify, request
from model import db, Users, Properties, Images


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
                    'location': rental.location,
                    'bedrooms': rental.bedrooms,
                    'price': rental.price,
                    'image': [image.filename for image in rental.images[0]] if images else []
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
