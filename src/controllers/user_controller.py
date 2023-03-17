try:
    from datetime import timedelta

    from flask import Blueprint, jsonify, request, abort
    from flask_jwt_extended import create_access_token

    from decorators.error_decorator import error_handlers
    from decorators.user_login import get_admin_user, get_user_fromdb
    from main import db, bcrypt
    from models.attending import Attending
    from models.user import User
    from schemas.attending_schema import attending_schema, \
        attending_schemas
    from schemas.user_schema import user_schema, UserSchema
except ImportError:
    print("Error has occurred with imports"
          "Please check importing from modules is correct")

# Creates blueprint for user controller
users = Blueprint("user", __name__, url_prefix="/users")


# Get method for accessing all users
# Initial user has to be admin 
# to be allowed to view the list of users
# method uses get_admin_user decorator, to validate and 
# return valid user object
# Method returns all user objects in JSON format
@users.route("/display_users", methods=["GET"])
@error_handlers
@get_admin_user
def get_users(**kwargs):
    """Return users from database
    
    Uses get_admin_decorator to return valid admin user
    Queries users from database and serialize information 
    into json format
    """
    users_list = User.query.all()

    result = UserSchema(only=\
                        ["id", "first_name", "last_name", "email"],\
                              many=True)

    return jsonify(result.dump(users_list))


# Get method for displaying single user, 
# including bands and venues they own
# route utilizes get_user_from db to return validated user object
# Queries user for display from route request
# returns user object serialized into json format
@users.route("/display_user/<int:user_id>", methods=["GET"])
@error_handlers
@get_user_fromdb
def display_user(**kwargs):
    """Return user information in json format
    
    Method utilizes get_user_fromdb
    queries user in database, checks if user id's match
    return serialized data, or error message and code
    """

    user = kwargs["user"]

    user_display = db.get_or_404(User, kwargs["user_id"],\
                                  description=\
                                    "User not found, please check id")

    if user.id != user_display.id:
        return jsonify({"message" : 
                        "Sorry you do not have access to this user"}),\
                              401

    return jsonify(user_schema.dump(user_display))


# Get method for displaying contents of attending table
# Route queries attending objects from database
# serializes through schema and returns json format of 
# attending table contents
@users.route("/attending/show", methods=["GET"])
@error_handlers
def get_attendees():
    """Return Attending objects from database"""


    attendees_list = Attending.query.all()

    result = attending_schemas.dump(attendees_list)

    return jsonify(result)


# Post method to allow users to login to the api
# route takes user email and password in json format, 
# returns user email and jwt token for access to sites functionality
@users.route("/login", methods=["POST"])
@error_handlers
def user_login():
    """Return user email and JWT token

    method queries user email and checks password is correct
    returns error if incorrect or grants access and returns
    JWT token and user email
    """


    # collect schema to load user request into json object
    user_fields = user_schema.load(request.json)

    user = User.query.filter_by(email=user_fields["email"]).first()

    if not user or not bcrypt\
    .check_password_hash(user.password, user_fields["password"]):
        return jsonify({"message" : \
                        "email or password didn't match"}),200
        
    
    expiry = timedelta(days=1)
    access_token = create_access_token(identity=str(user.id),\
                                        expires_delta=expiry)
    
    return jsonify({"user" : user.email, "token" : access_token}), 200


# Post method to register new user into database,
# Takes user fields through input via JSON on postman/insomnia
# Returns user token and registration message
@users.route("/register", methods=["POST"])
@error_handlers
def user_register():
    """Registers user in database

    method requires fields to be filled out in json format
    fields assign to user object 
    serialize through schema and stored in database
    returns user email and JWT access token
    """
    user_fields = user_schema.load(request.json)

    # Filter user emails to confirm email is not already in use
    user = User.query.filter_by(email=user_fields["email"]).first()
    # If email is in use, 
    # send error message to login or create new account
    if user:
        return abort(401, description="Email is already in use, \
                    please login with email or create a new account")
    
    user = User()

    user.first_name = user_fields["first_name"]
    user.last_name = user_fields["last_name"]
    user.email = user_fields["email"]
    user.password = bcrypt\
        .generate_password_hash(user_fields["password"])\
            .decode("utf-8")
    user.admin = False

    db.session.add(user)

    db.session.commit()
    
    
    expiry = timedelta(days=1)
    access_token = create_access_token(identity=str(user.id),\
                                        expires_delta=expiry)
    
    return jsonify({"user" : user.email, "token" : access_token}), 200


# Route for updating users details
# method utilizes get_user_fromdb to return validated user object
# Takes input via json format to assign updated details to user object
# returns updated user object in JSON format
@users.route("/update", methods=["PUT"])
@error_handlers
@get_user_fromdb
def update_user(**kwargs):
    """Updates user in database

    method requires user details to be updated and validated in schema
    return updated user object in JSON format
    """

    user_fields = user_schema.load(request.json)

    user = kwargs["user"]
    
    user.first_name = user_fields["first_name"]
    user.last_name = user_fields["last_name"]
    user.email = user_fields["email"]
    user.password = bcrypt\
        .generate_password_hash(user_fields["password"])\
            .decode("utf-8")
    user.admin = False

    db.session.commit()


    return jsonify(user_schema.dump(user))


# Route method to delete user from database
# method utilizes get_user_fromdb to return validated user object
# takes route request as id to query user object from database
# compares user id with authenticated user
# returns error if id's do not match
# otherwise user deletes from db 
# returns json message and 200 code
@users.route("/delete/<int:id>", methods=["DELETE"])
@get_user_fromdb
@error_handlers
def delete_user(**kwargs):
    """Deletes user from database"""

    user = kwargs["user"]

    id = kwargs["id"]

    if user.id != id:
        return abort(401, description="Invalid User, please check ID")
    elif user.admin and not user:
        db.session.delete(user)
        db.session.commit()
    else:
        db.session.delete(user)
        db.session.commit()

    return { "message" : "user deleted" }, 200


# Post method to allow users to attend an upcoming show
# route utilizes get_user_fromdb to return validated user object
# loads attending schema for serialization
# creates Attending instance and takes input via JSON format 
# to assign user id and show id to instance
# stores attending instance in database
# returns JSON format of attending instance
@users.route("/attending/register", methods=["POST"])
@get_user_fromdb
@error_handlers
def register_attendance(**kwargs):
    """Stores attending object in database"""

    user = kwargs["user"]

    attending_fields = attending_schema.load(request.json)

    attending = Attending()

    attending.user_id = user.id
    attending.show_id = attending_fields["show_id"]

    db.session.add(attending)
    db.session.commit()

    return jsonify(attending_schema.dump(attending))


# Delete method to allow users to remove attendance from a show
# method takes user identity and attending id
# removes attendance record and returns json message "attendance deleted"
@users.route("/attending/remove/<int:attending_id>",\
              methods=["DELETE"])
@get_user_fromdb
@error_handlers
def remove_attendance(**kwargs):
    """Removes attendance from database"""

    user = kwargs["user"]

    attending = db.get_or_404(Attending, kwargs["attending_id"],\
                               description="record not found")

    if user.id != attending.user_id:
        return {"message" : \
                 "Sorry you do not have access to this attendance"},\
                      401
    
    db.session.delete(attending)
    db.session.commit()

    return jsonify({"message" : "attendance removed"}), 200