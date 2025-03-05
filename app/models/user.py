from app.utils import db
from bson import ObjectId

class User:
    @staticmethod
    def create_user(data):
        new_user = {
            "name": data.get("name"),
            "email": data["email"],
            "password": data["password"],  # Hash passwords in real use
            "role": "user",
            "created_at": datetime.datetime.utcnow()
        }
        return db.users.insert_one(new_user).inserted_id

    @staticmethod
    def find_by_email(email):
        return db.users.find_one({"email": email})

    @staticmethod
    def find_by_id(user_id):
        return db.users.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def to_json(user):
        return {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "created_at": user["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        }
