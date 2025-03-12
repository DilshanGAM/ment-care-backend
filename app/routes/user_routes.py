from flask import Blueprint, request, jsonify
from app.utils import db
from app.services import *
from app.middleware import jwt_required
user_bp = Blueprint('user', __name__, url_prefix='/users')

# Sample user registration route
@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}) , 400
    status_code ,response  = create_user(data)
    return jsonify({"message": response}), status_code

@user_bp.route('/login', methods=['POST'])
def authenticate_user():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    status_code, response = login_user(data)
    return jsonify(response), status_code

@user_bp.route('/user', methods=['GET'])
@jwt_required
def get_user_info():
    status_code, response = get_user(request)
    return response, status_code
