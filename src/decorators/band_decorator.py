from flask import abort, jsonify
from functools import wraps
from models.band import Band


def get_band_fromdb(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            band_id = int(kwargs.get("band_id"))
            band = Band.query.filter_by(id=band_id).first_or_404(description="Sorry this band does not exist, please check id")

            kwargs["band"] = band

            return func(*args, **kwargs)
        except TypeError:
            return jsonify({"message" : "Please ensure you input a string"}), 500
        except ValueError:
            return jsonify({"message" : "Please ensure you input a number"}), 500
    return wrapper