try:
    from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
    from flask import jsonify
    from functools import wraps
    from models.user import User
except ImportError:
    print("Error has occurred with imports"
          "Please check importing from modules is correct")


# Admin decorator
# fetches admin user with the use of a JWT token
# verify_jwt_in_request ensures jwt is verfied
# User objects are queried using id=get_jwt_identity() 
# to get correct identity
# checks if user is admin, if not returns error
# returns admin user as 
# user=kwargs["user"]
def get_admin_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        verify_jwt_in_request()

        user = User.query\
            .filter_by(id=get_jwt_identity())\
                .first_or_404(description=\
                              "Error in retrieving user, \
                                please check the token")

        if not user.admin:
            return jsonify({"message" : "Error has occurred," \
                            " please ensure you are" \
                            " logging in as the admin"}), 401
        kwargs["user"] = user

        return func(*args, **kwargs)
    return wrapper


# User decorator
# gets user object and validates/authenticates with JWT token
# queries user objects with id=get_jwt_identity() to locate user 
# associated with JWT token
# returns user object as user=kwargs["user"]
def get_user_fromdb(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        

        user = User.query\
            .filter_by(id=get_jwt_identity())\
                .first_or_404(description=\
                              "Error in retrieving user," \
                                "please check the token")

        
        kwargs["user"] = user

        return func(*args, **kwargs)
    return wrapper
