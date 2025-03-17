from app.utils import db
import datetime
from flask import jsonify
from google import genai


gemini_api_key = "AIzaSyCz_tHvBZGPu_f2rruj3shdqxBGnAsBaBQ"

chat_collection = db.get_collection("chats")
def send_depression_message(request):
    user = request.user
    data = request.json
    if not user:
        return jsonify({"error": "No data provided"}), 400
    try:
        new_chat = {
            "email": user["email"],
            "message": data["message"],
            "role" : "user",
            "img" : data["url"],
            "created_at": datetime.datetime.now()
        }
        chat_collection.insert_one(new_chat)
        
        #get all chats for the user
        chats = chat_collection.find({"email": user["email"]})
        #convert the whole output in to a string with the sender date and message
        chat_string = ""
        for chat in chats:
            chat_string += chat["role"] + " " + str(chat["created_at"]) + " : " + chat["message"] + "\n"
              
        client = genai.Client(api_key=gemini_api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents="Assume you are depression patient helper and write a response for last message to continue this conversation. make the response very short and easy to read. Do not let the patient to feel that he or she is a patient." + data["message"]
        )
        new_message = response.text
        new_chat = {
            "email": user["email"],
            "message": new_message,
            "role" : "helper",
            "created_at": datetime.datetime.now()
        }
        chat_collection.insert_one(new_chat)
        #get all chats for the user
        chats = chat_collection.find({"email": user["email"]}, {"_id": 0})
        
        return jsonify(list(chats)), 201
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500

def get_all_chats(request):
    user = request.user
    if not user:
        return jsonify({"error": "No data provided"}), 400
    try:
        chats = chat_collection.find({"email": user["email"]}, {"_id": 0})
        return jsonify(list(chats)), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500