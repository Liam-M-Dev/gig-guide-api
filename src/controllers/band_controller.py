from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from decorators import error_handlers
from main import db
from models.band import Band
from models.playing import Playing
from models.user import User
from schemas.band_schema import band_schema, bands_schema
from schemas.playing_schema import playing_schema, playing_schemas


bands = Blueprint("bands", __name__, url_prefix="/bands")


# Get method for accessing all users and shows attendance,
# will implement Authorization in a bit and change attendance 
# from being viewable for admin
@bands.route("/", methods=["GET"])
def get_bands():

    bands_list = Band.query.all()

    result = bands_schema.dump(bands_list)

    return jsonify(result)


# Get request to return the list of bands that are playing shows
# Data to be returned is the band_id and show_id
@bands.route("/playing", methods=["GET"])
def get_bands_playing():

    playing_list = Playing.query.all()

    result = playing_schemas.dump(playing_list)

    return jsonify(result)


# Get method to return a single band
# Method takes an integer as the id number
# returns a json object with the band information,
# including associated shows they own/are playing
@bands.route("/display_single/<int:id>", methods=["GET"])
@error_handlers
def get_singe_band(id):
    
    band = db.get_or_404(Band, id, description="Band not found, please check id")

    return jsonify(band_schema.dump(band))


# Post method to create band within database
# method takes an integer as id number to authenticate user
# method takes band fields to serialize into database
# returns band fields as json object to confirm band creation
@bands.route("/create/<int:id>", methods=["POST"])
@jwt_required()
@error_handlers
def band_creation(id):

    user = get_jwt_identity()

    user = db.get_or_404(User, id, description="Invalid user, please check id")



    band_fields = band_schema.load(request.json)

    band = Band.query.filter_by(band_name=band_fields["band_name"]).first()
    if band:
        return abort(401, description="Sorry band name already in use")

    band = Band()

    band.band_name = band_fields["band_name"]
    band.genre = band_fields["genre"]
    band.state = band_fields["state"]
    band.user_id = user.id

    db.session.add(band)
    db.session.commit()

    return jsonify(band_schema.dump(band))


# Put method to update bands information
# requires jwt to allow user to update the band they own
# requires user identity to ensure user has access to the band
# takes user fields band name, genre, state
# returns json object of updated band
@bands.route("/update/<int:id>/<int:band_id>", methods=["PUT"])
@jwt_required()
@error_handlers
def update_band(id, band_id):
    user = get_jwt_identity()
    band_fields = band_schema.load(request.json)
    user = db.get_or_404(User, id, description="Invalid user, please check id")

    band = db.get_or_404(Band, band_id, description="Invalid band id, please check band id")

    

    if user.id != band.user_id:
        return abort(401, description="Sorry you do not have access to this band")
    
    band.band_name = band_fields["band_name"]
    band.genre = band_fields["genre"]
    band.state = band_fields["state"]
    band.user_id = band.user_id

    db.session.commit()

    return jsonify(band_schema.dump(band))
