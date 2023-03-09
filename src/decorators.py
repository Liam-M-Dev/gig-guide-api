from functools import wraps
from flask import abort
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import ProgrammingError


def error_handlers(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except ValidationError:
            return abort(401, description="Incorrect user fields entered \
                     Please enter first name, last name, \
                     email and password \
                     at least 8 characters long")
        except ProgrammingError:
            return abort(500, description="Database is not created, \
                            please create database and \
                            seed before continuing")
        return response
    return wrapper