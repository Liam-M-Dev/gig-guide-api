try:
    from main import ma
    from marshmallow import fields
except ImportError:
    print("Error has occurred with imports"
          "Please check importing from modules is correct")

class BandSchema(ma.Schema):
    class Meta:
        # fields to be exposed
        fields = ("id", "band_name", "genre", "state", "user", "shows", "playing")

    user = fields.Nested("UserSchema", only=["id", "first_name", "last_name"])
    shows = fields.List(fields.Nested("ShowSchema", only=["id", "show_name"]))
    playing = fields.List(fields.Nested("PlayingSchema", only=["show_id"]))


band_schema = BandSchema()
bands_schema = BandSchema(many=True)