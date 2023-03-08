from main import db


class Band(db.Model):
    __tablename__ = "BANDS"

    id = db.Column(db.Integer,primary_key=True)
    band_name = db.Column(db.String(),nullable=False)
    genre = db.Column(db.String(),nullable=False)
    state = db.Column(db.String(),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey("USERS.id"),
                        nullable=False)
    
    shows = db.relationship(
        "Show",
        backref="band",
        cascade="all, delete"
    )

    playing = db.relationship(
        "Playing",
        backref="band",
        cascade="all, delete"
    )
