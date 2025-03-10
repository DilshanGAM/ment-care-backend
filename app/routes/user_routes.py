from flask import Blueprint, request, jsonify
from app.utils import db
from app.services import *

user_bp = Blueprint('user', __name__, url_prefix='/users')

# Sample user registration route
@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}) , 400
    status_code ,response  = create_user(data)
    return jsonify({"message": response}), status_code 