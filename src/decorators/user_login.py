from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
import flask
from functools import wraps
import inspect
from main import db
from models.user import User

def get_admin_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        verify_jwt_in_request()

        user = User.query.filter_by(id=get_jwt_identity()).first_or_404()

        if not user.admin:
            return flask.abort(401, description="Unauthorized user, please login as admin to see user list")

        kwargs["user"] = user

        return func(*args, **kwargs)
    return wrapper


def get_user_fromdb(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        

        user = User.query.filter_by(id=get_jwt_identity()).first_or_404()

        
        kwargs["user"] = user

        return func(*args, **kwargs)
    return wrapper
