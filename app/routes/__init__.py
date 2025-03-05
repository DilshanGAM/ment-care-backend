from flask import Blueprint

# Import blueprints from different route files
from .user_routes import user_bp

# Create a list of all blueprints to be registered in the main app
blueprints = [user_bp]
