from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from decorators import error_handlers
from main import db
from models.band import Band
from models.show import Show
from models.venue import Venue
from models.user import User
from schemas.show_schema import show_schema, shows_schema, ShowSchema
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


# Post method to allow user to create a new show
# method requires venue id to authenticate venue
# method takes data input via fields for show name, date, band_id
# sets shows venue id to the venue id
# returns json object of show data
@shows.route("/create/show/venue/<int:id>", methods=["POST"])
@jwt_required()
@error_handlers
def show_creation(id):

    venue = get_jwt_identity()

    venue = db.get_or_404(Venue, id, description="Venue does not exist")

    show_fields = show_schema.load(request.json)

    show = Show.query.filter_by(show_name=show_fields["show_name"]).first()
    if show:
        return abort(401, description="Sorry this show already exists")

    show = Show()

    show.show_name = show_fields["show_name"]
    show.date = show_fields["date"]
    show.band_id = show_fields["band_id"]
    show.venue_id = venue.id

    db.session.add(show)
    db.session.commit()

    return jsonify(show_schema.dump(show))


# Post method to allow user to create a new show
# method requires venue id to authenticate venue
# method takes data input via fields for show name, date, band_id
# sets shows venue id to the venue id
# returns json object of show data
@shows.route("/create/show/venue/<int:id>", methods=["POST"])
@jwt_required()
@error_handlers
def show_creation(id):

    band = get_jwt_identity()

    band = db.get_or_404(Band, id, description="Band does not exist")

    show_fields = show_schema.load(request.json)

    show = Show.query.filter_by(show_name=show_fields["show_name"]).first()
    if show:
        return abort(401, description="Sorry this show already exists")

    show = Show()

    show.show_name = show_fields["show_name"]
    show.date = show_fields["date"]
    show.band_id = band.id
    show.venue_id = show_fields["show_id"]

    db.session.add(show)
    db.session.commit()

    return jsonify(show_schema.dump(show))