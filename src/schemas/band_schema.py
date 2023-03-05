from main import ma
from marshmallow import fields

class BandSchema(ma.Schema):
    class Meta:
        # fields to be exposed
        fields = ("id", "band_name", "genre", "state", "user")

    user = fields.Nested("UserSchema", only=("id", "first_name", "last_name"))


band_schema = BandSchema()
bands_schema = BandSchema(many=True)