from app.utils import db
import datetime
import bcrypt
import jwt
from flask import jsonify

# Secret key for JWT
JWT_SECRET = "your_secret_key"  # Change this to a secure, unpredictable secret in production
JWT_ALGORITHM = "HS256"

# Access the users collection
users_collection = db.get_collection("users")

def create_user(request):
    #check if the data["type"] is admin and the request.user is admin
    data = request.json
    if data["type"]=="admin" and request.user["type"] !="admin":
        return 403,"Only admins can create admin accounts"
    if data["type"]=="doctor" and request.user["type"] !="admin":
        return 403,"Only admins can create admin accounts"
    if request.user["type"] == "patient":
        return 403,"Patients are not allowed to create new user accounts"
    try:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), salt)
        new_user = {
            "email" : data["email"],
            "first_name" : data["first_name"],
            "last_name" : data["last_name"],
            "type" : data["type"],
            "password" : hashed_password,
            "salt": salt,
            "phone": data["phone"],
            "diseases" : data["diseases"],
            "image" : data["image"],
            "created_at": datetime.datetime.now()
        }
        existing_user = users_collection.find_one({"email": data["email"]})
        if existing_user:
            return 403, "User already exists"
        users_collection.insert_one(new_user).inserted_id
        return 201, "User registered successfully"
    except Exception as e:
        print(e)
        print("Error creating user")
        return 500, "Internal server error"





def login_user(data):
    try:
        # Find the user by email
        user = users_collection.find_one({"email": data["email"]})
        
        if not user:
            return 404, "User not found"
        
        # Validate the password
        print(user["password"])
        given_hash = bcrypt.hashpw(data["password"].encode('utf-8'), user["salt"])
        print(given_hash)
        if not given_hash == user["password"]:
            return 401, "Invalid credentials"
        
        # Payload for JWT
        payload = {
            "user_id": str(user["_id"]),
            "email": user["email"],
            "type": user["type"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "phone": user["phone"],
            "diseases": user["diseases"],
            "image": user["image"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)  # token expires in 2 hours
        }
        
        # Create JWT token
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        
        return 200, {
            "message": "Login successful",
            "token": token ,
            "user": {
                "email": user["email"],
                "type": user["type"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "phone": user["phone"],
                "diseases": user["diseases"],
                "image": user["image"],
            }
        }
        
    except Exception as e:
        print(e)
        print("Error logging in user")
        return 500, "Internal server error"

def get_user(request):
    user = request.user
    if not user:
        return 404, "User not found"
    return 200, jsonify(user)
def get_all_users_service(user):
    if user["type"] != "admin":
        return 403, "Unauthorized"
    try:
        users = users_collection.find({}, {"password": 0, "salt": 0 , "created_at": 0 , "_id": 0})
        users_list = list(users)
        return 200, jsonify(users_list)
    except Exception as e:
        print(e)
        print("Error getting users")
        return 500, "Internal server error"
def get_all_doctors_service(user):
    if user["type"] != "admin":
        return 403, "Unauthorized"
    try:
        doctors = users_collection.find({"type": "doctor"}, {"password": 0, "salt": 0 , "created_at": 0 , "_id": 0})
        doctors_list = list(doctors)
        return 200, jsonify(doctors_list)
    except Exception as e:
        print(e)
        print("Error getting doctors")
        return 500, "Internal server error"
def get_all_patients_service(user):
    #only doctor and admin can access
    if user["type"] != "admin" and user["type"] != "doctor":
        return 403, "Unauthorized"
    try:
        patients = users_collection.find({"type": "patient"}, {"password": 0, "salt": 0 , "created_at": 0 , "_id": 0})
        patients_list = list(patients)
        return 200, jsonify(patients_list)
    except Exception as e:
        print(e)
        print("Error getting patients")
        return 500, "Internal server error"
