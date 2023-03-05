from main import db


class Band(db.Model):

    __tablename__ = "BANDS"

    id = db.Column(db.Integer,primary_key=True)
    band_name = db.Column(db.String(),nullable=False)
    genre = db.Column(db.String(),nullable=False)
    state = db.Column(db.String(),nullable=False)
