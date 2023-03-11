from flask import Blueprint, jsonify, request, abort
from main import db
from models.venue import Venue
from models.show import Show
from schemas.venue_schema import venue_schema, venues_schema, VenueSchema
from schemas.show_schema import show_schema, ShowSchema



venues = Blueprint("venues", __name__, url_prefix="/venues")


# Get method for accessing all users and shows attendance,
# will implement Authorization in a bit and change attendance 
# from being viewable for admin
@venues.route("/", methods=["GET"])
def get_bands():

    venues_list = Venue.query.all()

    result = venues_schema.dump(venues_list)

    return jsonify(result)


# Get method to access one venue through id,
# Method takes venue id
# returns json object of venue data including upcoming shows
@venues.route("/display/venue/<int:id>", methods=["GET"])
def display_venue(id):

    venue = db.get_or_404(Venue, id, description="Invalid venue id, please check ID")

    venue_schema = VenueSchema(only=["id", "venue_name", "location"])

    upcoming_shows = db.get_or_404(Show, venue.id, description="There are no upcoming shows")

    show_schema = ShowSchema(only=["show_name", "date"])

    

    return jsonify(venue_schema.dump(venue), show_schema.dump(upcoming_shows))