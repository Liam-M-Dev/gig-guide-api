from main import db
from flask import Blueprint
from models.user import User

db_commands = Blueprint("db", __name__)

@db_commands .cli.command("create")
def create_db():
    db.create_all()
    print("Tables Created")


@db_commands .cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables Dropped")