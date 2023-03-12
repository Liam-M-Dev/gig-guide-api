from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from decorators import error_handlers
from main import db
from models.venue import Venue
from models.user import User
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

    venue_display = VenueSchema(only=["id", "venue_name", "location"])

    upcoming_shows = db.get_or_404(Show, venue.id, description="There are no upcoming shows")

    show_display = ShowSchema(only=["show_name", "date"])

    return jsonify(venue_display.dump(venue), show_display.dump(upcoming_shows))


# Post method to allow user to create a new venue
# method requires user id to authenticate user
# method takes data input via fields for venue name, location
# sets venue user id to the users id
# returns json object of venue data
@venues.route("/register/<int:id>", methods=["POST"])
@jwt_required()
@error_handlers
def venue_creation(id):

    user = get_jwt_identity()

    user = db.get_or_404(User, id, description="Invalid user, please check id")
    
    venue_fields = venue_schema.load(request.json)

    venue = Venue.query.filter_by(venue_name=venue_fields["venue_name"]).first()
    if venue:
        return abort(401, description="Sorry this venue already exists")

    venue = Venue()

    venue.venue_name = venue_fields["venue_name"]
    venue.location = venue_fields["location"]
    venue.user_id = user.id

    db.session.add(venue)
    db.session.commit()

    return jsonify(venue_schema.dump(venue))


# Put method to allow users to update venue
# method takes user identity and venue identity
# user identity is to authenticate and ensure user is authorized to access venue
# fields are edited via input of dictionary data
# returns updated venue information as json object
@venues.route("/update/<int:user_id>/<int:venue_id>", methods=["PUT"])
@jwt_required()
@error_handlers
def update_venue(user_id, venue_id):
    user = get_jwt_identity()
    venue_fields = venue_schema.load(request.json)
    user = db.get_or_404(User, user_id, description="Invalid user, please check id")

    venue = db.get_or_404(Venue, venue_id, description="Invalid venue id, please check venue id")

    

    if user.id != venue.user_id:
        return abort(401, description="Sorry you do not have access to this venue")
    
    venue.venue_name = venue_fields["venue_name"]
    venue.location = venue_fields["location"]
    venue.user_id = user.id

    db.session.commit()

    return jsonify(venue_schema.dump(venue))

# Delete route to allow a user to delete their venue
# requires user id and venue id plus jwt authentication
# checks that user owns venue before deletion or user is an admin
# deletes venue and returns json format of message "venue deleted"
@venues.route("/delete/<int:user_id>/<int:venue_id>", methods=["DELETE"])
@jwt_required()
@error_handlers
def delete_venue(user_id, venue_id):

    user = get_jwt_identity()

    user = db.get_or_404(User, user_id, description="Invalid user, please check id")

    venue = db.get_or_404(Venue, venue_id, description="Invalid venue id, please check venue id")

    if user.id != venue.user_id and not user.admin:
        return abort(401, description="Sorry you do not have access to this venue")
    elif user.admin and not user.id != venue.user_id:
        db.session.delete(venue)
        db.session.commit()
    else:
        db.session.delete(venue)
        db.session.commit()

    return jsonify({"msg": "venue deleted"})