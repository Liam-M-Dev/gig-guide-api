try:
    from flask import Blueprint, jsonify, request

    from decorators.error_decorator import error_handlers
    from decorators.show_decorator import get_show_fromdb
    from decorators.user_login import get_user_fromdb
    
    from main import db

    from models.band import Band
    from models.show import Show
    from models.venue import Venue

    from schemas.show_schema import show_schema, shows_schema, \
        ShowSchema
    from schemas.venue_schema import VenueSchema
except ImportError:
    print("Error has occurred with imports"
          "Please check importing from modules is correct")


shows = Blueprint("shows", __name__, url_prefix="/shows")


# Get method for accessing shows in show table
# Returns show objects as list of JSON objects
@shows.route("/", methods=["GET"])
@error_handlers
def get_shows():
    """Returns shows within show table"""

    shows_list = Show.query.all()

    result = shows_schema.dump(shows_list)

    return jsonify(result)


# Get method for accessing a single show
# method takes show Id 
# returns show including the venue it has a relationship with
@shows.route("/display/show/<int:id>", methods=["GET"])
@error_handlers
def display_show(id):
    """Returns a single show object with 
    venue object associated with show
    
    queries show with route header request of id integer
    queries venue with show.venue_id
    """


    show = db.get_or_404(Show, id, description=\
                         "Sorry no shows found with this id")
    venue = db.get_or_404(Venue, show.venue_id, description=\
                          "Venue does not exist for this show")


    show_display = ShowSchema(only=["id", "show_name", "date"])
    venue_display = VenueSchema(only=["venue_name", "location"])

    return jsonify(show_display.dump(show), venue_display.dump(venue))


# Get route using search method to 
# display shows with similar venue or band
# uses requests to query show with venue_id or band_id
# returns validated shows in JSON object format
@shows.route("/display/search", methods=["GET"])
@error_handlers
def search_shows():
    """Returns shows with matching venue or band ids
    
    uses requests within route to query show associating id
    with the given venue or band id
    """
    shows_list = []

    if request.args.get("venue"):
        shows_list = Show.query.filter_by(venue_id = \
                                          request.args.get("venue"))
    elif request.args.get("band"):
        shows_list = Show.query.filter_by(band_id = \
                                          request.args.get("band"))
    else:
        return jsonify({"message" : \
                        "Incorrect search parameters, \
                            please use band or venue"}), 400

    shows_display = ShowSchema(only=["show_name", "date"], many=True)

    return jsonify(shows_display.dump(shows_list))


# Post method to allow user to create a new show
# gets validated user from get_user_fromdb
# uses input via show_fields to associate fields with attributes
# adds show object to shows table
# returns created show in JSON object format
@shows.route("/create/show/", methods=["POST"])
@error_handlers
@get_user_fromdb
def show_creation(**kwargs):
    """Creates show object and stores in shows table
    
    takes requests within route to associate if venue
    or band is creating the show
    attributes venue or band id to show.venue_id or show.band_id
    adds newly created show object to shows table
    """

    user = kwargs["user"]

    show_fields = show_schema.load(request.json)
    
    show = Show()

    if request.args.get("venue"):
        venue = Venue.query\
            .filter_by(id=request.args.get("venue"))\
                .first_or_404(description=\
                              "Sorry this venue does not exist, \
                                please check id")
        
        if venue.user_id != user.id:
            return jsonify({"message": \
                            "Sorry you do not have access \
                                to this venue to create a show"}), 401

        show.show_name = show_fields["show_name"]
        show.date = show_fields["date"]
        show.band_id = show_fields["band_id"]
        show.venue_id = venue.id
    elif request.args.get("band"):
        band = Band.query\
            .filter_by(id=request.args.get("band"))\
                .first_or_404(description=\
                              "Sorry this band does not exist, \
                              please check id")

        if band.user_id != user.id:
            return jsonify({"message": \
                            "Sorry you do not have access \
                                to this band to create a show"}), 401
        
        show.show_name = show_fields["show_name"]
        show.date = show_fields["date"]
        show.band_id = band.id
        show.venue_id = show_fields["venue_id"]

    show_exists = Show.query\
        .filter_by(show_name=show_fields["show_name"]).first()
    if show_exists:
        return jsonify({"message" : "Show already exists"}), 401
    
    db.session.add(show)
    db.session.commit()


    return jsonify(show_schema.dump(show))


# Put method to allow venues to update show
# gets validated user from get_user_fromdb
# gets validated show from get_show_fromdb
# uses request to confirm if venue or band is updating show
# uses show_fields to associate fields with show attributes
# commits updated show to db
# returns updated show object in JSON object format
@shows.route("/update/show/<int:show_id>", methods=["PUT"])
@get_user_fromdb
@get_show_fromdb
@error_handlers
def update_show(**kwargs):

    user = kwargs["user"]

    show = kwargs["show"]

    show_fields = show_schema.load(request.json)

    if request.args.get("venue"):

        venue = Venue.query\
            .filter_by(id=request.args.get("venue"))\
                .first_or_404(description=\
                              "Sorry this venue does not exist, \
                                please check id")
        
        if venue.user_id != user.id:
            return jsonify({"message": \
                            "Sorry you do not have access \
                                to this venue to update a show"}), 401

        if venue.id != show.venue_id:
            return jsonify({"message" : \
                            "You do not have access to this show"}), \
                                401
        
        show.show_name = show_fields["show_name"]
        show.date = show_fields["date"]
        show.band_id = show_fields["band_id"]
        show.venue_id = venue.id
    elif request.args.get("band"):
        band = Band.query\
            .filter_by(id=request.args.get("band"))\
                .first_or_404(description="Sorry this band does \
                              not exist, please check id")

        if band.user_id != user.id:
            return jsonify({"message": \
                            "Sorry you do not have access to this \
                                band to update a show"}), 401
        
        show.show_name = show_fields["show_name"]
        show.date = show_fields["date"]
        show.band_id = band.id
        show.venue_id = show_fields["venue_id"]
    

    db.session.commit()

    return jsonify(show_schema.dump(show))


# Delete route to allow a user to delete their venue
# gets validated user from get_user_fromdb
# gets validated show from get_show_fromdb
# uses requests within route to confirm if venue or band
# is deleting show
# confirms venue/band have the authorized user.id to do this
# deletes show from shows table
# returns JSON message show deleted with 200 code
@shows.route("/delete/show/<int:show_id>", methods=["DELETE"])
@get_user_fromdb
@get_show_fromdb
@error_handlers
def delete_show_venue(**kwargs):
    """Delete show from shows table
    
    method uses requests within route to identify
    if band or venue are making the request
    deletes show from shows table
    """

    user = kwargs["user"]
    show = kwargs["show"]

    if request.args.get("venue"):
        venue = Venue.query\
            .filter_by(id=request.args.get("venue"))\
                .first_or_404(description=\
                              "Sorry this venue does not exist\
                              , please check id")
        if venue.user_id != user.id:
            return jsonify({"message" : \
                            "Sorry you do not have access \
                                to this venue to delete the show"}), \
                                    401
        if venue.id != show.venue_id:
            return jsonify({"message" : \
                            "Sorry venue does not have access \
                                to the show for deletion"}), 401
    
        db.session.delete(show)
    elif request.args.get("band"):
        band = Band.query\
            .filter_by(id=request.args.get("band"))\
                .first_or_404(description=\
                              "Sorry band does not exist, check id")
        if band.user_id != user.id:
            return jsonify({"message" : \
                            "Sorry you do not have access to this band \
                                to delete the show"}), 401
        if band.id != show.band_id:
            return jsonify({"message" : \
                            "Sorry band does not have access \
                                to show for deletion"}), 401
        db.session.delete(show)
    
    db.session.commit()

    return jsonify({"msg": "show deleted"}), 200
