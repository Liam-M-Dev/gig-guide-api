from flask import Blueprint, jsonify, request, abort
from main import db
from models.band import Band
from models.show import Show
from models.venue import Venue
from schemas.show_schema import show_schema, shows_schema, ShowSchema
from schemas.band_schema import BandSchema
from schemas.venue_schema import VenueSchema



shows = Blueprint("shows", __name__, url_prefix="/shows")


# Get method for accessing all users and shows attendance,
# will implement Authorization in a bit and change attendance 
# from being viewable for admin
@shows.route("/", methods=["GET"])
def get_bands():

    shows_list = Show.query.all()

    result = shows_schema.dump(shows_list)

    return jsonify(result)


# Get method for accessing a single show
# method takes show Id 
# returns show including the venue
@shows.route("/display/show/<int:id>", methods=["GET"])
def display_show(id):

    show = db.get_or_404(Show, id, description="Sorry no shows found with this id")
    venue = db.get_or_404(Venue, show.venue_id, description="Venue does not exist for this show")


    show_display = ShowSchema(only=["id", "show_name", "date"])
    venue_display = VenueSchema(only=["venue_name", "location"])

    return jsonify(show_display.dump(show), venue_display.dump(venue))