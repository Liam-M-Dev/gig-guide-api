try:
    from flask import Blueprint, jsonify, request

    from decorators.error_decorator import error_handlers
    from decorators.band_decorator import get_band_fromdb
    from decorators.user_login import get_user_fromdb
    
    from main import db

    from models.band import Band
    from models.playing import Playing
    from models.show import Show

    from schemas.band_schema import band_schema, bands_schema,\
          BandSchema
    from schemas.playing_schema import playing_schema,\
          playing_schemas
except ImportError:
    print("Error has occurred with imports"
          "Please check importing from modules is correct")

bands = Blueprint("bands", __name__, url_prefix="/bands")


# Get method for accessing all bands in database
# returns bands from database in JSON format
@bands.route("/", methods=["GET"])
@error_handlers
def get_bands():
    """Returns bands from database in JSON format"""

    bands_list = Band.query.all()

    result = bands_schema.dump(bands_list)

    return jsonify(result)


# Get request to return the list of bands that are playing shows
# Data to be returned is playing objects in JSON format
@bands.route("/playing", methods=["GET"])
@error_handlers
def get_bands_playing():
    """Returns all playing objects from playing table"""
    playing_list = Playing.query.all()

    result = playing_schemas.dump(playing_list)

    return jsonify(result)


# Get method to return a single band
# Method utilizes get_band_fromdb to return validated band
# Returns a band from the the band table
@bands.route("/display/band/<int:band_id>", methods=["GET"])
@error_handlers
@get_band_fromdb
def get_single_band(**kwargs):
    """Returns band object from database"""

    band = kwargs["band"]

    return jsonify(band_schema.dump(band))


# Get method to allow search of bands with similar genre
# or similar states
# Takes request from query
# Queries bands from database and returns band objects
# that have the same data in either genre or state fields
@bands.route("/display/search", methods=["GET"])
@error_handlers
def genre_list_bands():
    """Returns queried bands from database
    
    Method uses requests to search for bands with
    similar genres or states in database
    """
    band_list = []

    if request.args.get("genre"):
        band_list = Band.query.filter_by(genre=\
                                          request.args.get("genre"))
    elif request.args.get("state"):
        band_list = Band.query.filter_by(state=\
                                          request.args.get("state"))
    else:
        return jsonify({"message" :\
                         "Incorrect search parameters, \
                              please use genre or state"}),\
                              400

    band_display = BandSchema(only=["band_name", "shows"], many=True)

    return jsonify(band_display.dump(band_list))


# Post method to create band within database
# fetches user using get_user_fromdb to return validated user
# loads band_schema for marshmallow validation
# uses input in JSON format for band fields to assign information
# to band instance
# returns created band in JSON format
@bands.route("/create", methods=["POST"])
@error_handlers
@get_user_fromdb
def band_creation(**kwargs):
    """Create band instance within database
    
    Method uses band_schema to associate fields
    with band model attributes
    validates and returns created band
    """

    user = kwargs["user"]

    band_fields = band_schema.load(request.json)

    band = Band.query.filter_by(band_name=band_fields["band_name"])\
        .first()
    if band:
        return jsonify({"message" : "Band name already exists"}), 400

    band = Band()

    band.band_name = band_fields["band_name"]
    band.genre = band_fields["genre"]
    band.state = band_fields["state"]
    band.user_id = user.id

    db.session.add(band)
    db.session.commit()

    return jsonify(band_schema.dump(band))


# Put method to update bands information
# gets validated user from get_user_fromdb
# gets validated band from get_band_fromdb
# uses JSON input to associate fields with band attributes
# stores updated band in database
# returns updated band object in JSON format
@bands.route("/update/<int:band_id>", methods=["PUT"])
@error_handlers
@get_user_fromdb
@get_band_fromdb
def update_band(**kwargs):
    """Updates band object within band table
    
    Uses band_schema to associate fields with band attributes
    commits updated band to database
    returns updated band in JSON format
    """

    user = kwargs["user"]

    band_fields = band_schema.load(request.json)
    
    band = kwargs["band"]

    if user.id != band.user_id:
        return jsonify({"message" : \
                        "Sorry you do not have access to this band"}),\
                              401
    
    band.band_name = band_fields["band_name"]
    band.genre = band_fields["genre"]
    band.state = band_fields["state"]
    band.user_id = band.user_id

    db.session.commit()

    return jsonify(band_schema.dump(band))


# Delete route to allow a user to delete their band
# gets validated user from get_user_fromdb
# gets validated band from get_band_fromdb
# Checks that band.user_id and user.id match
# returns error if they do not match
# deletes band from database
# returns band deleted message in JSON format and 200 code
@bands.route("/delete/<int:band_id>", methods=["DELETE"])
@error_handlers
@get_user_fromdb
@get_band_fromdb
def delete_band(**kwargs):

    user = kwargs["user"]
    band = kwargs["band"]

    if user.id != band.user_id and not user.admin:
        return jsonify({"message" : \
                        "Sorry you do not have access to this band"}),\
                        401
    elif user.admin and user.id != band.user_id:
        db.session.delete(band)
        db.session.commit()
    else:
        db.session.delete(band)
        db.session.commit()

    return jsonify({"message": "band deleted"}), 200


# Post route to allow bands to register themselves to an upcoming gig
# gets validated user from get_user_fromdb
# gets validated band from get_band_fromdb
# checks that user.id matches band.user_id
# takes input in JSON format 
# to associate playing fields with playing attributes
# stores playing object in playing table
# returns json object of playing with band id and show id
@bands.route("/playing/register/<int:band_id>", methods=["POST"])
@error_handlers
@get_user_fromdb
@get_band_fromdb
def register_to_show(**kwargs):

    user = kwargs["user"]
    band = kwargs["band"]

    if user.id != band.user_id:
        return jsonify({"message" :\
                        "Sorry you do not have access to this band"}),\
                         401
    
    playing_fields = playing_schema.load(request.json)
    playing = Playing()

    playing.band_id = band.id
    playing.show_id = playing_fields["show_id"]

    show = Show.query.filter_by(id=playing_fields["show_id"]).first()
    if not show:
        return jsonify({"message" : \
                "Sorry this show does not exist, please check id"}), \
                    404

    db.session.add(playing)
    db.session.commit()

    return jsonify(playing_schema.dump(playing))


# Delete method to allow bands 
# to remove themselves from playing a show
# gets validated user from get_user_fromdb
# gets validated band from get_band_fromdb
# gets playing_id and queries through playing table 
# to find playing object
@bands.route("/playing/remove/<int:band_id>/<int:playing_id>",\
              methods=["DELETE"])
@error_handlers
@get_user_fromdb
@get_band_fromdb
def remove_playing(**kwargs):
    """Removes playing object from playing table"""

    user = kwargs["user"]
    band = kwargs["band"]

    if user.id != band.user_id:
        return jsonify({"message" : \
                        "Sorry you do not have access to this band"}),\
                              401
    
    playing_id = kwargs["playing_id"]

    playing = db.get_or_404(Playing, \
                            playing_id, \
                            description=\
                                "something went wrong, please check id")
    
    if playing.band_id != band.id:
        return jsonify({"message" : \
                        "Sorry you do not have access to this record"}), \
                            401

    db.session.delete(playing)
    db.session.commit()

    return jsonify({"message" : "Removed from up coming show"}), 200