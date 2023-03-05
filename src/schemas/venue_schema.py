from main import ma
from marshmallow import fields

class VenueSchema(ma.Schema):
    class Meta:
        # fields to be exposed
        fields = ("id", "venue_name", "location", "user")

    user = fields.Nested("UserSchema", only=("id", "first_name", "last_name"))


venue_schema = VenueSchema()
venues_schema = VenueSchema(many=True)