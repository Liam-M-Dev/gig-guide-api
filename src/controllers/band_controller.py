from flask import Blueprint, jsonify, request, abort
from main import db
from models.band import Band
from schemas.band_schema import band_schema, bands_schema



bands = Blueprint("bands", __name__, url_prefix="/bands")


# Get method for accessing all users and shows attendance,
# will implement Authorization in a bit and change attendance 
# from being viewable for admin
@bands.route("/", methods=["GET"])
def get_bands():

    bands_list = Band.query.all()

    result = bands_schema.dump(bands_list)

    return jsonify(result)