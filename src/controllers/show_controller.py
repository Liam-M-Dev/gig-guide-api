from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from decorators.error_decorator import error_handlers
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
def get_shows():

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


@shows.route("/display/search", methods=["GET"])
@error_handlers
def search_shows():

    shows_list = []

    if request.args.get("venue"):
        shows_list = Show.query.filter_by(venue_id = request.args.get("venue"))
    elif request.args.get("band"):
        shows_list = Show.query.filter_by(band_id = request.args.get("band"))

    shows_display = ShowSchema(only=["show_name", "date"], many=True)

    return jsonify(shows_display.dump(shows_list))


# Post method to allow user to create a new show
# method requires venue id to authenticate venue
# method takes data input via fields for show name, date, band_id
# sets shows venue id to the venue id
# returns json object of show data
@shows.route("/create/show/venue/<int:id>", methods=["POST"])
@jwt_required()
@error_handlers
def show_creation_venue(id):

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
@shows.route("/create/show/band/<int:id>", methods=["POST"])
@jwt_required()
@error_handlers
def show_creation_band(id):

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
    show.venue_id = show_fields["venue_id"]

    db.session.add(show)
    db.session.commit()

    return jsonify(show_schema.dump(show))


# Put method to allow venues to update show
# method takes venue identity and show identity
# venue identity is to authenticate and ensure venue is authorized to access show
# fields are edited via input of dictionary data
# returns updated show information as json object
@shows.route("/update/show/venue/<int:venue_id>/<int:show_id>", methods=["PUT"])
@jwt_required()
@error_handlers
def update_show_venue(venue_id, show_id):
    venue = get_jwt_identity()
    show_fields = show_schema.load(request.json)
    
    venue = db.get_or_404(Venue, venue_id, description="Invalid venue id, please check venue id")

    show = db.get_or_404(Show, show_id, description="Show does not exist, please check id")

    if venue.id != show.venue_id:
        return abort(401, description="Sorry you do not have access to this show")
    
    show.show_name = show_fields["show_name"]
    show.date = show_fields["date"]
    show.band_id = show_fields["band_id"]
    show.venue_id = venue.id
    

    db.session.commit()

    return jsonify(show_schema.dump(show))


# Put method to allow bands to update show
# method takes band identity and show identity
# band identity is to authenticate and ensure band is authorized to access show
# fields are edited via input of dictionary data
# returns updated show information as json object
@shows.route("/update/show/band/<int:band_id>/<int:show_id>", methods=["PUT"])
@jwt_required()
@error_handlers
def update_show_band(band_id, show_id):
    band = get_jwt_identity()
    show_fields = show_schema.load(request.json)
    
    band = db.get_or_404(Band, band_id, description="Invalid band id, please check band id")

    show = db.get_or_404(Show, show_id, description="Show does not exist, please check id")

    if band.id != show.band_id:
        return abort(401, description="Sorry you do not have access to this show")
    
    show.show_name = show_fields["show_name"]
    show.date = show_fields["date"]
    show.band_id = band.id
    show.venue_id = show_fields["venue_id"]
    

    db.session.commit()

    return jsonify(show_schema.dump(show))


# Delete route to allow a user to delete their venue
# requires user id and venue id plus jwt authentication
# checks that user owns venue before deletion or user is an admin
# deletes venue and returns json format of message "venue deleted"
@shows.route("/delete/show/venue/<int:venue_id>/<int:show_id>", methods=["DELETE"])
@jwt_required()
@error_handlers
def delete_show_venue(venue_id, show_id):

    venue = get_jwt_identity()

    show = db.get_or_404(Show, show_id, description="Show does not exist, please check id")

    venue = db.get_or_404(Venue, venue_id, description="Invalid venue id, please check venue id")

    if venue.id != show.venue_id:
        return abort(401, description="Sorry you do not have access to this show")
    
    db.session.delete(show)
    db.session.commit()

    return jsonify({"msg": "show deleted"})


# Delete route to allow a user to delete their venue
# requires user id and venue id plus jwt authentication
# checks that user owns venue before deletion or user is an admin
# deletes venue and returns json format of message "venue deleted"
@shows.route("/delete/show/band/<int:band_id>/<int:show_id>", methods=["DELETE"])
@jwt_required()
@error_handlers
def delete_show_band(band_id, show_id):

    band = get_jwt_identity()

    show = db.get_or_404(Show, show_id, description="Show does not exist, please check id")

    band = db.get_or_404(Band, band_id, description="Invalid venue id, please check band id")

    if band.id != show.band_id:
        return abort(401, description="Sorry you do not have access to this show")
    
    db.session.delete(show)
    db.session.commit()

    return jsonify({"msg": "show deleted"})