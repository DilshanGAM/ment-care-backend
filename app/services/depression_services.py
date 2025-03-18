from app.utils import db
import datetime
from flask import jsonify
from google import genai
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
import requests
from io import BytesIO
import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from app.models.attention_layer import AttentionLayer

with open("./app/models/tokenizer.pickle", "rb") as handle:
    tokenizer = pickle.load(handle)

# Emotion class indices (reverse lookup)
class_indices = {
    0: 'angry',
    1: 'disgusted',
    2: 'fearful',
    3: 'happy',
    4: 'neutral',
    5: 'sad',
    6: 'surprised'
}
#model is in app/models/vgg19_best_image_model.h5
image_model = load_model("./app/models/vgg19_best_image_model.h5")
text_model = load_model("./app/models/text-model.h5" , custom_objects={"AttentionLayer": AttentionLayer})

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

def predict_emotions_from_image_url(img_url):
    try:
        # Step 1: Download image from URL
        response = requests.get(img_url)
        if response.status_code != 200:
            return 400, "Failed to fetch image from URL"

        img_data = BytesIO(response.content)

        # Step 2: Preprocess image
        img = image.load_img(img_data, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Step 3: Predict emotions using the image model
        emotion_probs = image_model.predict(img_array)[0]  # Shape: (num_classes,)
        
        # Step 4: Map predictions to emotion labels
        emotions_result = {class_indices[i]: float(prob) for i, prob in enumerate(emotion_probs)}

        # Step 5: Calculate depression score
        depressed_emotions = ['angry', 'fearful', 'sad']
        depression_score = sum([emotions_result[emotion] for emotion in depressed_emotions])

        # Step 6: Build JSON response
        response_data = {
            "status": "success",
            "emotions": emotions_result,
            "depression_score": round(depression_score, 4),
            "is_depressed": depression_score > 0.5  # Adjust threshold as needed
        }

        return 200, jsonify(response_data)

    except Exception as e:
        print("Error processing image prediction:", e)
        return 500, "Internal server error"

def predict_depression_from_text_service(message):
    try:
        # Validate input
        if not message or message.strip() == "":
            return 400, "Message cannot be empty"

        # Step 1: Preprocess and tokenize the input message
        sequence = tokenizer.texts_to_sequences([message])
        padded_sequence = pad_sequences(sequence, maxlen=4000, padding='post')

        # Step 2: Predict probability using the text model
        probability = text_model.predict(padded_sequence)[0][0]  # Single output
        
        # Step 3: Build JSON response
        response_data = {
            "status": "success",
            "input_message": message,
            "depression_probability": float(probability)
        }

        return 200, jsonify(response_data)

    except Exception as e:
        print("Error predicting depression from text:", e)
        return 500, "Internal server error"

