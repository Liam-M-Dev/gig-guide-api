from flask import Blueprint, jsonify, request, abort
from main import db
from models.venue import Venue
from schemas.venue_schema import venue_schema, venues_schema



venues = Blueprint("venues", __name__, url_prefix="/venues")


# Get method for accessing all users and shows attendance,
# will implement Authorization in a bit and change attendance 
# from being viewable for admin
@venues.route("/", methods=["GET"])
def get_bands():

    venues_list = Venue.query.all()

    result = venues_schema.dump(venues_list)

    return jsonify(result)