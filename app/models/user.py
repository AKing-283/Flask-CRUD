from marshmallow import Schema, fields, validate, EXCLUDE, ValidationError
from bson import ObjectId
from datetime import datetime

# Custom ObjectId field for Marshmallow (if needed)
class ObjectIdField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return str(value) if value else None

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return ObjectId(value)
        except Exception:
            raise ValidationError("Invalid ObjectId.")

# Marshmallow Schema
class UserSchema(Schema):
    id = ObjectIdField(attribute="_id", dump_only=True)  # handles Mongo _id
    name = fields.String(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6), load_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    class Meta:
        unknown = EXCLUDE

# Python Data Model
class User:
    def __init__(self, name, email, password, _id=None, created_at=None, updated_at=None):
        self._id = _id or ObjectId()
        self.name = name
        self.email = email
        self.password = password
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    @staticmethod
    def from_db(user_data):
        if not user_data:
            return None
        return User(
            _id=user_data.get('_id'),
            name=user_data.get('name'),
            email=user_data.get('email'),
            password=user_data.get('password'),
            created_at=user_data.get('created_at'),
            updated_at=user_data.get('updated_at')
        )

    def to_dict(self):
        return {
            "_id": self._id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
