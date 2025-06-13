from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_restful import Api
from dotenv import load_dotenv
import os

from app.routes.user_routes import UserResource, UserListResource
from app.utils.logger import setup_logger

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure app
app.config['MONGO_URI'] = 'mongodb://mongodb:27017/userdb'
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')

# Initialize extensions
CORS(app)
mongo = PyMongo(app)
app.extensions['mongo'] = mongo
bcrypt = Bcrypt(app)
api = Api(app)

# Setup logger
logger = setup_logger()

# Register routes
api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<string:user_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)