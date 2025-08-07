from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from routes.expense_routes import expense_bp

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Import and register blueprints
from routes.auth_routes import auth_bp
app.register_blueprint(auth_bp, url_prefix="/api/auth")

# TODO: Add expense_routes in the future
from routes.expense_routes import expense_bp
app.register_blueprint(expense_bp, url_prefix="/api/expenses")

if __name__ == "__main__":
    app.run(debug=True)
