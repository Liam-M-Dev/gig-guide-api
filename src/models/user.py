from main import db


class User(db.Model):
    __tablename__ = "USERS"

    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(),nullable=False)
    last_name = db.Column(db.String(),nullable=False)
    email = db.Column(db.String(),unique=True,nullable=False)
    password = db.Column(db.String(),nullable=False)
    admin = db.Column(db.Boolean(), default=False)

    bands = db.relationship(
        "Band",
        backref="user",
        cascade="all, delete"
    )
    venues = db.relationship(
        "Venue",
        backref="user",
        cascade="all, delete"
    )
    attending = db.relationship(
        "Attending",
        backref="user",
        cascade="all, delete"
    )
