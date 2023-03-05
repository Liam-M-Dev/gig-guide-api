from main import db, bcrypt
from flask import Blueprint
from models.user import User
from models.band import Band
from models.venue import Venue
from models.show import Show
from models.attending import Attending

db_commands = Blueprint("db", __name__)


@db_commands .cli.command("create")
def create_db():
    db.create_all()
    print("Tables Created")


@db_commands .cli.command("seed")
def seed_db():
    # User seeds
    user1 = User(
        # attributes
        first_name = "User",
        last_name = "Admin",
        email = "test@test.com.au",
        password = bcrypt.generate_password_hash("password123").decode("utf-8"),
        admin = True
    )
    db.session.add(user1)
    db.session.commit()
    print("table seeded")


@db_commands .cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables Dropped")