try:
    from flask import Blueprint, jsonify, request

    from decorators.error_decorator import error_handlers
    from decorators.user_login import get_user_fromdb
    from decorators.venue_decorator import get_venue_fromdb

    from main import db

    from models.show import Show
    from models.venue import Venue

    from schemas.show_schema import ShowSchema
    from schemas.venue_schema import venue_schema, venues_schema, \
        VenueSchema
except ImportError:
    print("Error has occurred with imports"
          "Please check importing from modules is correct")


venues = Blueprint("venues", __name__, url_prefix="/venues")


# Get method for accessing all venues
# returns all venues from venue table in JSON format
@venues.route("/", methods=["GET"])
@error_handlers
def get_venues():
    """Returns all venues from venue table"""

    venues_list = Venue.query.all()

    result = venues_schema.dump(venues_list)

    return jsonify(result)


# Get method to display one venue and its upcoming shows,
# queries venue using route request of venue id integer
# queries shows that has the venue id
# returns json object of venue data including upcoming shows
@venues.route("/display/venue/<int:id>", methods=["GET"])
@error_handlers
def display_venue(id):
    """Returns venue and upcoming shows in JSON format
    
    queries venue with request from route header
    queries shows using venue.id
    serializes venue and show objects through schemas
    """
    venue = Venue.query.filter_by(id=id).first()

    if not venue:
        return jsonify({"message" : \
                        "Sorry venue does not exist"}), 400

    venue_display = VenueSchema(only=["id", "venue_name", "location"])

    upcoming_shows = Show.query\
        .filter_by(venue_id = venue.id)
    
    if not upcoming_shows:
        upcoming_shows = []

    show_display = ShowSchema(only=["show_name", "date"], many=True)

    return jsonify(venue_display.dump(venue), \
                   show_display.dump(upcoming_shows))


# Post method to allow user to create a new venue
# gets validated user from user_from_db
# takes input using fields to associate with venue attributes
# returns registered venue in JSON format
@venues.route("/register/", methods=["POST"])
@error_handlers
@get_user_fromdb
def venue_creation(**kwargs):
    """Creates venue in venue table"""

    user = kwargs["user"]

    venue_fields = venue_schema.load(request.json)

    venue = Venue.query\
        .filter_by(venue_name=venue_fields["venue_name"]).first()
    if venue:
        return jsonify({"message" : "Sorry venue already exists"}), 401

    venue = Venue()

    venue.venue_name = venue_fields["venue_name"]
    venue.location = venue_fields["location"]
    venue.user_id = user.id

    db.session.add(venue)
    db.session.commit()

    return jsonify(venue_schema.dump(venue))


# Put method to allow users to update venue
# gets validated user from get_user_fromdb
# gets validated venue from get_venue_fromdb
# checks that venue.user_id and user.id match
# if not, returns error with JSON message and error code
# else, takes input via venue fields to match with attributes
# returns updated venue information in JSON format
@venues.route("/update/<int:venue_id>", methods=["PUT"])
@error_handlers
@get_user_fromdb
@get_venue_fromdb
def update_venue(**kwargs):
    """Updates venue object and commits to db
    
    method uses venue_fields to associate with venue attributes
    """

    user = kwargs["user"]
    venue = kwargs["venue"]

    venue_fields = venue_schema.load(request.json)
    

    if user.id != venue.user_id:
        return jsonify({"message" : \
                        "You do not have access to this venue"}), \
                            401
    
    venue.venue_name = venue_fields["venue_name"]
    venue.location = venue_fields["location"]
    venue.user_id = user.id

    db.session.commit()

    return jsonify(venue_schema.dump(venue))


# Delete route to allow a user to delete their venue
# gets validated user from get_user_fromdb
# gets validated venue from get_venue_fromdb
# checks if venue.user_id matches user.id
# if not returns error with JSON message and error code
# else, deletes venue from venue table
# returns message venue deleted
@venues.route("/delete/<int:venue_id>", methods=["DELETE"])
@error_handlers
@get_user_fromdb
@get_venue_fromdb
def delete_venue(**kwargs):
    """Deletes venue from venue table"""


    user = kwargs["user"]
    venue = kwargs["venue"]

    if user.id != venue.user_id and not user.admin:
        return jsonify({"message" : \
                        "You do not have access to this venue"}), \
                            401
    elif user.admin and user.id != venue.user_id:
        db.session.delete(venue)
        db.session.commit()
    else:
        db.session.delete(venue)
        db.session.commit()

    return jsonify({"msg": "venue deleted"}), 200