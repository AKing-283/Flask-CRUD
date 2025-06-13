from flask import current_app
from pymongo import MongoClient

client = None
db = None

def init_db(app):
    global client, db
    from .config import Config
    app.config.from_object(Config)
    client = MongoClient(app.config["MONGO_URI"])
    db = client.get_default_database()

def get_users_collection():
    return db["users"]
