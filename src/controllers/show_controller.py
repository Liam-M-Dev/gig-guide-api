from flask import Blueprint, jsonify, request, abort
from main import db
from models.show import Show
from schemas.show_schema import show_schema, shows_schema



shows = Blueprint("shows", __name__, url_prefix="/shows")


# Get method for accessing all users and shows attendance,
# will implement Authorization in a bit and change attendance 
# from being viewable for admin
@shows.route("/", methods=["GET"])
def get_bands():

    shows_list = Show.query.all()

    result = shows_schema.dump(shows_list)

    return jsonify(result)