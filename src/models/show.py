from main import db


class Show(db.Model):
    __tablename__ = "SHOWS"

    id = db.Column(db.Integer,primary_key=True)
    show_name = db.Column(db.String(),nullable=False)
    date = db.Column(db.String(),nullable=False)
    band_id = db.Column(db.Integer,db.ForeignKey("BANDS.id"),
                        nullable=False)
    venue_id = db.Column(db.Integer,db.ForeignKey("VENUES.id"),
                        nullable=False)
