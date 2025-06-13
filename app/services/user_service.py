from datetime import datetime
from bson import ObjectId
from flask import current_app
from app.models.user import User, UserSchema
from app.utils.exceptions import ResourceNotFoundError, DuplicateResourceError

class UserService:
    def __init__(self, mongo):
        self.mongo = mongo
        self.user_schema = UserSchema()

    def get_all_users(self):
        users = self.mongo.db.users.find()
        return [User.from_db(user) for user in users]

    def get_user_by_id(self, user_id):
        try:
            user = self.mongo.db.users.find_one({'_id': ObjectId(user_id)})
            if not user:
                raise ResourceNotFoundError(f'User with id {user_id} not found')
            return User.from_db(user)
        except Exception as e:
            current_app.logger.error(f'Error fetching user: {str(e)}')
            raise

    def create_user(self, user_data):
        try:
            # Validate user data
            validated_data = self.user_schema.load(user_data)
            
            # Check if email already exists
            if self.mongo.db.users.find_one({'email': validated_data['email']}):
                raise DuplicateResourceError('Email already exists')

            # Hash password
            from flask_bcrypt import generate_password_hash
            validated_data['password'] = generate_password_hash(validated_data['password']).decode('utf-8')
            
            # Add timestamps
            validated_data['created_at'] = datetime.utcnow()
            validated_data['updated_at'] = datetime.utcnow()

            # Insert user
            result = self.mongo.db.users.insert_one(validated_data)
            return self.get_user_by_id(str(result.inserted_id))

        except Exception as e:
            current_app.logger.error(f'Error creating user: {str(e)}')
            raise

    def update_user(self, user_id, user_data):
        try:
            # Validate user exists
            existing_user = self.get_user_by_id(user_id)

            # Validate update data
            validated_data = self.user_schema.load(user_data, partial=True)
            
            # Hash password if provided
            if 'password' in validated_data:
                from flask_bcrypt import generate_password_hash
                validated_data['password'] = generate_password_hash(validated_data['password']).decode('utf-8')

            # Update timestamp
            validated_data['updated_at'] = datetime.utcnow()

            # Update user
            self.mongo.db.users.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': validated_data}
            )
            return self.get_user_by_id(user_id)

        except Exception as e:
            current_app.logger.error(f'Error updating user: {str(e)}')
            raise

    def delete_user(self, user_id):
        try:
            # Validate user exists
            self.get_user_by_id(user_id)

            # Delete user
            result = self.mongo.db.users.delete_one({'_id': ObjectId(user_id)})
            if result.deleted_count == 0:
                raise ResourceNotFoundError(f'User with id {user_id} not found')
            return True

        except Exception as e:
            current_app.logger.error(f'Error deleting user: {str(e)}')
            raise