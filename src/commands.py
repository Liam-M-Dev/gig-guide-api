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

    user2 = User(
        # attributes
        first_name = "Fred",
        last_name = "Snow",
        email = "fredSnow@randomemail.com",
        password = bcrypt.generate_password_hash("happythirty2").decode("utf-8"),   
    )
    db.session.add(user2)

    user3 = User(
        # attributes
        first_name = "Cherry",
        last_name = "Greer",
        email = "cherrygreer43@randomemail.com",
        password = bcrypt.generate_password_hash("feeling0k!").decode("utf-8"),   
    )
    db.session.add(user3)

    user4 = User(
        # attributes
        first_name = "Chad",
        last_name = "Oneill",
        email = "thechad3212@randomemail.com",
        password = bcrypt.generate_password_hash("musiclover").decode("utf-8"),   
    )
    db.session.add(user4)

    user5 = User(
        # attributes
        first_name = "Irene",
        last_name = "Potts",
        email = "Irenesttop@randomemail.com",
        password = bcrypt.generate_password_hash("anotherpassword").decode("utf-8"),   
    )
    db.session.add(user5)

    db.session.commit()

    band1 = Band(
        band_name = "Amyl and the Sniffers",
        genre = "Punk",
        state = "VIC",
        user_id = 2,
    )
    db.session.add(band1)

    band2 = Band(
        band_name = "Uboa",
        genre = "Noise",
        state = "VIC",
        user_id = 2,
    )
    db.session.add(band2)

    band3 = Band(
        band_name = "Kilat",
        genre = "Black Metal",
        state = "VIC",
        user_id = 2,
    )
    db.session.add(band3)

    band4 = Band(
        band_name = "Speed",
        genre = "Hardcore",
        state = "NSW",
        user_id = 4,
    )
    db.session.add(band4)

    band5 = Band(
        band_name = "Blind Girls",
        genre = "Hardcore",
        state = "QLD",
        user_id = 5,
    )
    db.session.add(band5)

    db.session.commit()

    venue1 = Venue(
        venue_name = "The Old Bar",
        location = "74-75 Johnson St, Fitzroy, VIC",
        user_id = 3,
    )
    db.session.add(venue1)

    venue2 = Venue(
        venue_name = "Northcote Social Club",
        location = "301 High st, Northcote, VIC",
        user_id = 3,
    )
    db.session.add(venue2)

    venue3 = Venue(
        venue_name = "John Curtain Hotel",
        location = "29 Lygon St, Carlton, VIC",
        user_id = 3,
    )
    db.session.add(venue3)

    venue4 = Venue(
        venue_name = "Mary's Underground",
        location = "29 Reiby Pl, Sydney, NSW",
        user_id = 4,
    )
    db.session.add(venue4)

    venue5 = Venue(
        venue_name = "The Sewing Room Perth",
        location = "317 Murray St, Perth, WA",
        user_id = 5,
    )
    db.session.add(venue5)

    db.session.commit()

    print("table seeded")


@db_commands .cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables Dropped")