from flask import abort, jsonify
from functools import wraps
from models.venue import Venue


def get_venue_fromdb(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            venue_id = int(kwargs.get("venue_id"))
            venue = Venue.query.filter_by(id=venue_id).first_or_404(description="Sorry this venue does not exist, please check id")

            kwargs["venue"] = venue

            return func(*args, **kwargs)
        except TypeError:
            return jsonify({"message" : "Please ensure you input a string"}), 500
        except ValueError:
            return jsonify({"message" : "Please ensure you input a number"}), 500
    return wrapper