from main import db


class Show(db.Model):
    __tablename__ = "SHOWS"

    id = db.Column(db.Integer,primary_key=True)
    show_name = db.Column(db.String(),nullable=False)
    date = db.Column(db.String(),nullable=False)
    band_id = db.Column(db.Integer,db.ForeignKey("BANDS.id", ondelete="SET NULL"), nullable=True)
    venue_id = db.Column(db.Integer,db.ForeignKey("VENUES.id", ondelete="SET NULL"), nullable=True)
    
    attending = db.relationship(
        "Attending",
        backref="show",
        cascade="all, delete"
    )

    playing = db.relationship(
        "Playing",
        backref="show",
        cascade="all, delete"
    )
