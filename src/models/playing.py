from main import db


class Playing(db.Model):
    __tablename__ = "PLAYING"

    id = db.Column(db.Integer,primary_key=True)
    band_id = db.Column(db.Integer,db.ForeignKey("BANDS.id"),
                     nullable=False)
    show_id = db.Column(db.Integer,db.ForeignKey("SHOWS.id"),
                     nullable=False)

