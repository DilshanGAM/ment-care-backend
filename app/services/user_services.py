from app.utils import db
import datetime
import bcrypt

# Access the users collection
users_collection = db.get_collection("users")

def create_user(data):
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

    