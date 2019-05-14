from flask import Blueprint
from models.users import User
from flask_jwt jwt_required

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    return "USERS API"

@users_api_blueprint.route('/<username>', methods=['GET'])
def show(username):
    user = User.get_or_none(User.username == username)

    if not user:
        resp = {
            'message': 'No user with this name was found',
            'ok': False
        }

        return jsonify(resp)

    resp = {
        'message': 'Found the user with this username',
        'ok': True,
        'user': {
            'is': user.id,
            'username': user.username,
            'email': user.email
        },
        'ok': True
    }

    return jsonify(resp)
            