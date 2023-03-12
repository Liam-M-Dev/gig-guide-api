from main import ma
from marshmallow import fields

class ShowSchema(ma.Schema):
    class Meta:
        # fields to be exposed
        fields = ("id", "show_name", "date", "band_id", "venue_id")

    band = fields.Nested("BandSchema", only=["id", "band_name"])
    venue = fields.Nested("VenueSchema", only=["id", "venue_name"])


show_schema = ShowSchema()
shows_schema = ShowSchema(many=True)