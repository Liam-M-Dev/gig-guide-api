from flask import Blueprint, jsonify, request, abort
from main import db
from models.band import Band
from models.playing import Playing
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