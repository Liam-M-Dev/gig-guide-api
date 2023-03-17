try:
    from functools import wraps
    from flask import jsonify
    from marshmallow.exceptions import ValidationError
    from sqlalchemy.exc import ProgrammingError, DataError
except ImportError:
    print("Error has occurred with imports"
          "Please check importing from modules is correct")

# Error handler decorator to catch various errors within server and client
def error_handlers(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except ValidationError:
            return jsonify({"message" : "Error with validation, ensure all fields are filled out correctly"}), 400
        except ProgrammingError:
            return jsonify({"message" : "Database is not created, please create and seed database first"}), 500
        except TypeError:
            return jsonify({"message" : "TypeError within the server"}), 500
        except DataError:
            return jsonify({"message" : "Error with the data you are inputting"}), 400
        return response
    return wrapper

