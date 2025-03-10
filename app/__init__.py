from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app.routes import blueprints

load_dotenv()

app = Flask(__name__)
CORS(app)


for bp in blueprints:
    app.register_blueprint(bp)
    
if __name__ == '__main__':
    app.run(debug=True)