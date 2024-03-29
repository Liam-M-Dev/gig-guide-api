try:
    from main import db
except ImportError:
    print("Error has occurred with imports"
          "Please check importing from modules is correct")

class Venue(db.Model):
    __tablename__ = "VENUES"

    id = db.Column(db.Integer,primary_key=True)
    venue_name = db.Column(db.String(),nullable=False)
    location = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey("USERS.id"),
                        nullable=False)
    
    shows = db.relationship(
        "Show",
        backref="venue",
        cascade="all, delete"
    )
