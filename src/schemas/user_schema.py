from main import ma
from marshmallow.validate import Length

class UserSchema(ma.Schema):
    class Meta:
        #fields to be exposed
        fields = ("id", "first_name", "last_name", "email", "password", "admin")

    password = ma.String(validate=Length(min=8))

user_schema = UserSchema()
users_schema = UserSchema(many=True)