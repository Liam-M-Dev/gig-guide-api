from main import ma
from marshmallow import fields

class PlayingSchema(ma.Schema):
    class Meta:
        fields = ("id", "band_id", "show_id")

    band_id = fields.Nested("BandSchema", only=["id"])
    show_id = fields.Nested("ShowSchema", only=["id"])