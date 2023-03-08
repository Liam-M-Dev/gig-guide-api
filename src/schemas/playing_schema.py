from main import ma
from marshmallow import fields


class PlayingSchema(ma.Schema):
    class Meta:
        fields = ("id", "band_id", "show_id")



playing_schema = PlayingSchema()
playing_schemas = PlayingSchema(many=True)