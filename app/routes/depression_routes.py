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
@depression_bp.route('/predict-emotion', methods=['POST'])
def predict_emotion():
    data = request.json
    img_url = data.get("img_url")    
    statuscode,response = predict_emotions_from_image_url(img_url)
    return response,statuscode
@depression_bp.route('/predict-text', methods=['POST'])
def predict_text():
    data = request.json
    text = data.get("message")    
    statuscode,response = predict_depression_from_text_service(text)
    return response,statuscode

