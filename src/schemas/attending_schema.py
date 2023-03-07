from main import ma
from marshmallow import fields


class AttendingSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "show_id")



attending_schema = AttendingSchema()
attending_schemas = AttendingSchema(many=True)