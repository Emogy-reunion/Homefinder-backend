from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from model import db, Users, Images, Properties
from sqlalchemy.orm import selectingload


posts = Blueprint('posts', __name__)


@posts.routes('/member_uploads_preview', methods=['GET'])
@jwt_required()
def member_uploads_preview():
    '''
    loads posts posted by a specific user
    '''

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    user_id = get_jwt_identity()
    listings = Properties.query.filter_by(user_id=user_id).options(selectinload(Properties.images))
    paginated_results = listings.paginate(page=page, per_page=per_page)
    
    properties = []
    for item in paginated_results.items:
        properties.append({
                'id': item.id,
                'location': item.location,
                'price': item.price,
                'bedrooms': item.bedrooms,
                'image': [image.filename for image in item.images[0]] if images else []
                })

    response = {
            'properties': properties,
            'pagination': {
                "total": paginated_results.total,
                "page": paginated_results.page,
                "pages": paginated_results.pages,
                "per_page": paginated_results.per_page,
                "next": paginated_results.next_num if paginated_results.has_next else None
                "prev": paginated_results.prev_num if paginated_results.has_prev else None
                }
            }
    return jsonify(response)


@posts.routes('/member_uploads_details/<int:property_id>', methods=['GET'])
def member_upload_details():
    '''
    Retrieves an items details e.g map, description, images
