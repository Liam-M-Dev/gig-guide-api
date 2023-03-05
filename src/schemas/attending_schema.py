from main import ma
from marshmallow import fields


class AttendingSchema(ma.Schema):
    class Meta:
        fields = ("user", "shows")

    users = fields.Nested("UserSchema", only="id")
    shows = fields.Nested("ShowSchema", only="id")


