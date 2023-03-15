from flask_jwt_extended import jwt_required, get_jwt_identity
import flask
from functools import wraps
import inspect
from main import db
from models.user import User

def get_admin_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        user_id = int(kwargs.get("id"))

        user = db.session.query(User).filter_by(id=user_id).first_or_404(description="User not found, please check id")

        if not user.admin:
            return flask.abort(401, description="Unauthorized user, please login as admin to see user list")

        flask.g.user = user

        return func(*args, **kwargs)
    return wrapper


def get_user_fromdb(func):
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user = get_jwt_identity()
        user_id = int(kwargs.get("user_id"))
        user = db.session.query(User).filter_by(id=user_id).first_or_404(description="User not found, please check id")
        
        flask.g.user = user

        params = inspect.signature(func).parameters

        if "user" in params:
            return func(user=user, *args, **kwargs)
        else: 
            return func(*args, **kwargs)
    return wrapper
