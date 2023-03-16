from flask import Blueprint, jsonify, request, abort
from decorators.error_decorator import error_handlers
from decorators.user_login import get_user_fromdb
from decorators.band_decorator import get_band_fromdb
import json
from main import db
from models.band import Band
from models.playing import Playing
from models.show import Show
from schemas.band_schema import band_schema, bands_schema, BandSchema
from schemas.playing_schema import playing_schema, playing_schemas


bands = Blueprint("bands", __name__, url_prefix="/bands")


# Get method for accessing all users and shows attendance,
# will implement Authorization in a bit and change attendance 
# from being viewable for admin
@bands.route("/", methods=["GET"])
@error_handlers
def get_bands():

    bands_list = Band.query.all()

    result = bands_schema.dump(bands_list)

    return jsonify(result)


# Get request to return the list of bands that are playing shows
# Data to be returned is the band_id and show_id
@bands.route("/playing", methods=["GET"])
@error_handlers
def get_bands_playing():

    playing_list = Playing.query.all()

    result = playing_schemas.dump(playing_list)

    return jsonify(result)


# Get method to return a single band
# Method takes an integer as the id number
# returns a json object with the band information,
# including associated shows they own/are playing
@bands.route("/display/band/<int:band_id>", methods=["GET"])
@error_handlers
@get_band_fromdb
def get_single_band(**kwargs):
    
    band = kwargs["band"]

    return jsonify(band_schema.dump(band))


# Get method to return bands that play a similar genre of music
# method takes a string as the genre of music
# returns list of json object bands with name, genre and state
@bands.route("/display/search", methods=["GET"])
@error_handlers
def genre_list_bands():

    band_list = []

    if request.args.get("genre"):
        band_list = Band.query.filter_by(genre= request.args.get("genre"))
    elif request.args.get("state"):
        band_list = Band.query.filter_by(state= request.args.get("state"))
    else:
        return jsonify({"message" : "Incorrect search parameters, please use genre or state"}), 400

    band_display = BandSchema(only=["band_name", "shows"], many=True)

    return jsonify(band_display.dump(band_list))


# Post method to create band within database
# method takes an integer as id number to authenticate user
# method takes band fields to serialize into database
# returns band fields as json object to confirm band creation
@bands.route("/create", methods=["POST"])
@error_handlers
@get_user_fromdb
def band_creation(**kwargs):

    user = kwargs["user"]

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
@bands.route("/update/<int:band_id>", methods=["PUT"])
@error_handlers
@get_user_fromdb
@get_band_fromdb
def update_band(**kwargs):
    user = kwargs["user"]

    band_fields = band_schema.load(request.json)
    
    band = kwargs["band"]

    if user.id != band.user_id:
        return abort(401, description="Sorry you do not have access to this band")
    
    band.band_name = band_fields["band_name"]
    band.genre = band_fields["genre"]
    band.state = band_fields["state"]
    band.user_id = band.user_id

    db.session.commit()

    return jsonify(band_schema.dump(band))


# Delete route to allow a user to delete their band
# requires user id and band id plus jwt authentication
# checks that user owns band before deletion
# deletes band and returns message of band deleted
@bands.route("/delete/<int:band_id>", methods=["DELETE"])
@error_handlers
@get_user_fromdb
@get_band_fromdb
def delete_band(**kwargs):

    user = kwargs["user"]
    band = kwargs["band"]

    if user.id != band.user_id and not user.admin:
        return abort(401, description="Sorry you do not have access to this band")
    elif user.admin and not user.id != band.user_id:
        db.session.delete(band)
        db.session.commit()
    else:
        db.session.delete(band)
        db.session.commit()

    return {"message": "band deleted"}, 200


# Post route to allow bands to register themselves to an upcoming gig
# method takes the bands id and the show id they wish to register too
# returns json object of playing with band id and show id
@bands.route("/playing/register/<int:band_id>", methods=["POST"])
@error_handlers
@get_user_fromdb
@get_band_fromdb
def register_to_show(**kwargs):

    user = kwargs["user"]
    band = kwargs["band"]

    if user.id != band.user_id:
        return abort(401, description="Sorry you do not have access to this band")
    
    playing_fields = playing_schema.load(request.json)
    playing = Playing()

    playing.band_id = band.id
    playing.show_id = playing_fields["show_id"]

    show = Show.query.filter_by(id=playing_fields["show_id"]).first()
    if not show:
        return {"message" : "Sorry this show does not exist, please check id"}, 404

    db.session.add(playing)
    db.session.commit()

    return jsonify(playing_schema.dump(playing))


# Delete method to allow bands to remove themselves from playing a show
# method takes user id and band id to authenticate and ensure access to band
# returns message of removed from show to let the band know it has gone through
@bands.route("/playing/remove/<int:band_id>/<int:playing_id>", methods=["DELETE"])
@error_handlers
@get_user_fromdb
@get_band_fromdb
def remove_playing(**kwargs):
    
    user = kwargs["user"]
    band = kwargs["band"]

    if user.id != band.user_id:
        return {"message" : "Sorry you do not have access to this band"}, 401
    
    playing_id = kwargs["playing_id"]

    playing = db.get_or_404(Playing, playing_id, description="something went wrong, please check id")
    
    if playing.band_id != band.id:
        return {"message" : "Sorry you do not have access to this record"}, 401

    db.session.delete(playing)
    db.session.commit()

    return {"message" : "Removed from up coming show"}, 200