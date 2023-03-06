from main import db


class Playing(db.Model):
    __tablename__ = "PLAYING"

    id = db.Column(db.Integer,primary_key=True)
    band = db.Column(db.Integer,nullable=False)
    show = db.Column(db.Integer,nullable=False)