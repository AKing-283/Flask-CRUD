from flask import current_app
from flask_restful import Resource, reqparse
from app.services.user_service import UserService
from app.models.user import UserSchema
from app.utils.exceptions import ResourceNotFoundError, DuplicateResourceError

class UserListResource(Resource):
    def __init__(self):
        self.user_service = UserService(current_app.extensions['mongo'])
        self.user_schema = UserSchema()

    def get(self):
        """Get all users"""
        try:
            users = self.user_service.get_all_users()
            return {'users': [self.user_schema.dump(user) for user in users]}, 200
        except Exception as e:
            current_app.logger.error(f'Error in GET /users: {str(e)}')
            return {'message': 'Internal server error'}, 500

    def post(self):
        """Create a new user"""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name is required')
        parser.add_argument('email', type=str, required=True, help='Email is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')
        
        try:
            args = parser.parse_args()
            user = self.user_service.create_user(args)
            return self.user_schema.dump(user), 201
        except DuplicateResourceError as e:
            return {'message': str(e)}, 409
        except Exception as e:
            current_app.logger.error(f'Error in POST /users: {str(e)}')
            return {'message': 'Internal server error'}, 500

class UserResource(Resource):
    def __init__(self):
        self.user_service = UserService(current_app.extensions['mongo'])
        self.user_schema = UserSchema()

    def get(self, user_id):
        """Get a specific user"""
        try:
            user = self.user_service.get_user_by_id(user_id)
            return self.user_schema.dump(user), 200
        except ResourceNotFoundError as e:
            return {'message': str(e)}, 404
        except Exception as e:
            current_app.logger.error(f'Error in GET /users/{user_id}: {str(e)}')
            return {'message': 'Internal server error'}, 500

    def put(self, user_id):
        """Update a specific user"""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        
        try:
            args = parser.parse_args()
            # Remove None values
            args = {k: v for k, v in args.items() if v is not None}
            
            user = self.user_service.update_user(user_id, args)
            return self.user_schema.dump(user), 200
        except ResourceNotFoundError as e:
            return {'message': str(e)}, 404
        except Exception as e:
            current_app.logger.error(f'Error in PUT /users/{user_id}: {str(e)}')
            return {'message': 'Internal server error'}, 500

    def delete(self, user_id):
        """Delete a specific user"""
        try:
            self.user_service.delete_user(user_id)
            return '', 204
        except ResourceNotFoundError as e:
            return {'message': str(e)}, 404
        except Exception as e:
            current_app.logger.error(f'Error in DELETE /users/{user_id}: {str(e)}')
            return {'message': 'Internal server error'}, 500