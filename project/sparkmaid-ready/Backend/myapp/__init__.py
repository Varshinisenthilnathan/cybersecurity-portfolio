from flask import Flask
import os
from .routes.customer_routes import customer_bp
from .routes.maid_routes import maid_bp
from .routes.admin_routes import admin_bp
from .routes.auth_routes import auth_bp
from .routes.booking_routes import booking_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    CORS(app, supports_credentials=True, origins=["http://127.0.0.1:5500", "http://127.0.0.1:5000"])
    # Register Blueprints for modular routes
    app.register_blueprint(customer_bp)
    app.register_blueprint(maid_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(booking_bp) 
    
    return app
