from flask import Blueprint, request, jsonify
from app.utils import db
from app.services import *
from app.middleware import jwt_required
depression_bp = Blueprint('depression', __name__, url_prefix='/depression')

@depression_bp.route('/chat', methods=['POST'])
@jwt_required
def chat():
    response,status_code = send_depression_message(request)
    return response, status_code

@depression_bp.route('/chats', methods=['GET'])
@jwt_required
def chats():
    response,status_code = get_all_chats(request)
    return response, status_code
