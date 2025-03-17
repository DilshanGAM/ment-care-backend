import jwt
from functools import wraps
from flask import request, jsonify

JWT_SECRET = "your_secret_key"  # Use environment variable in production!
JWT_ALGORITHM = "HS256"

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        # Extract token from "Authorization" header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        
        try:
            decoded_payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            # Attach user data to the request context
            request.user = decoded_payload
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token!"}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function
