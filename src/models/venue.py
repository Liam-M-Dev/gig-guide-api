from main import db


class Venue(db.Model):

    __tablename__ = "VENUES"

    id = db.Column(db.Integer,primary_key=True)
    venue_name = db.Column(db.String(),nullable=False)
    location = db.Column(db.String(), nullable=False)
