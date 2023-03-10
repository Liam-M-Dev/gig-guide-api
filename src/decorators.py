from functools import wraps
from flask import abort
from flask_jwt_extended import get_jwt_identity
from main import db
from models.user import User
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import ProgrammingError

# Error handler decorator to catch various errors within server and client
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


# User Id decorator to get user identity
# def get_user_id(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         user = get_jwt_identity()

#         user = db.get_or_404(User, id, description="User not found, please check id")
#         func(*args, *kwargs)
