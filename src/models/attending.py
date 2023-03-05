from main import db


class Attending(db.Model):
    __tablename__ = "ATTENDING"

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("USERS.id"),
                        nullable=False)
    show_id = db.Column(db.Integer,db.ForeignKey("SHOWS.id"),
                        nullable=False)