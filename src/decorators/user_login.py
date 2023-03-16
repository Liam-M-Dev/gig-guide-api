from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask import abort
from functools import wraps
from models.user import User

def get_admin_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        verify_jwt_in_request()

        user = User.query.filter_by(id=get_jwt_identity()).first_or_404(description="Error in retrieving user, please check the token")

        if not user.admin:
            return abort(401, description="Unauthorized user, please login as admin to see user list")

        kwargs["user"] = user

        return func(*args, **kwargs)
    return wrapper


def get_user_fromdb(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        

        user = User.query.filter_by(id=get_jwt_identity()).first_or_404(description="Error in retrieving user, please check the token")

        
        kwargs["user"] = user

        return func(*args, **kwargs)
    return wrapper
