from functools import wraps
from flask import abort
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import ProgrammingError

# Error handler decorator to catch various errors within server and client
def error_handlers(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except ValidationError:
            return abort(401, description="Validation error, \
                          something has gone wrong \
                          with the fields you have inputted please \
                          check format and try again")
        except ProgrammingError:
            return abort(500, description="Database is not created, \
                            please create database and \
                            seed before continuing")
        return response
    return wrapper

