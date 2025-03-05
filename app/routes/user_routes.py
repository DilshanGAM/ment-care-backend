from flask import Blueprint, request, jsonify
from app.models.user import User
from app.utils import db

user_bp = Blueprint('user', __name__, url_prefix='/users')

# Sample user registration route
@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.json
    if not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400

    existing_user = db.users.find_one({"email": data["email"]})
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    new_user = {
        "name": data.get("name"),
        "email": data["email"],
        "password": data["password"],  # Hash password in real use
        "role": "user"
    }
    db.users.insert_one(new_user)

    return jsonify({"message": "User registered successfully"}), 201


# Sample user login route
@user_bp.route('/login', methods=['POST'])
def login_user():
    data = request.json
    user = db.users.find_one({"email": data["email"]})
    if not user or user["password"] != data["password"]:  # Use hashed password check
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({"message": "Login successful", "user": user["email"]})


# Sample protected route (requires authentication)
@user_bp.route('/profile', methods=['GET'])
def user_profile(current_user):
    return jsonify({
        "name": current_user["name"],
        "email": current_user["email"],
        "role": current_user["role"]
    })
