from main import ma
from marshmallow.validate import Length
from marshmallow import fields

class UserSchema(ma.Schema):
    class Meta:
        #fields to be exposed
        fields = ("id", "first_name", "last_name", "email", "password", "admin", "attending")

    attending = fields.List(fields.Nested("AttendingSchema", only=["show_id"]))
    password = ma.String(validate=Length(min=8))
    

user_schema = UserSchema()
users_schema = UserSchema(many=True)