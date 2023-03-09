from flask import Blueprint, jsonify, request, abort
from functools import wraps
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import ProgrammingError
from main import db, bcrypt
from models.user import User
from models.attending import Attending
from schemas.user_schema import user_schema, users_schema
from schemas.attending_schema import attending_schema, attending_schemas


users = Blueprint("user", __name__, url_prefix="/users")



# Get method for accessing all users and shows attendance,
# will implement Authorization in a bit and change attendance 
# from being viewable for admin
@users.route("/", methods=["GET"])
def get_users():

    users_list = User.query.all()

    result = users_schema.dump(users_list)

    return jsonify(result)


# Get method for displaying contents of attending table
@users.route("/attending/show")
def get_attendees():

    attendees_list = Attending.query.all()

    result = attending_schemas.dump(attendees_list)

    return jsonify(result)


# Post method to allow users to login to the api
# returns user details and JSON web token for authentication
@users.route("/login", methods=["POST"])
def user_login():
    # collect schema to load user request into json object
    user_fields = user_schema.load(request.json)

    user = User.query.filter_by(email=user_fields["email"]).first()

    if not user or not bcrypt\
    .check_password_hash(user.password, user_fields["password"]):
        return abort(401, "Incorrect password or email")
    
    return "Password accepted"


# Post method to register new user into database,
# Takes user fields through input via JSON on postman/insomnia
# Returns user token and registration message
@users.route("/register", methods=["POST"])
def user_register():
    # try except block to handle validation errors within schema
    try:
        user_fields = user_schema.load(request.json)

        
        # Filter user emails to confirm email is not already in use
        user = User.query.filter_by(email=user_fields["email"]).first()
        # If email is in use, send error message to login or create new account
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
        
        
        return jsonify(user_schema.dump(user))
    
    except ValidationError:
        return abort(401, description="Incorrect user fields entered \
                     Please enter first name, last name \
                     , email and password \
                     at least 8 characters long")
    except ProgrammingError:
            return abort(500, description="Database is not created, \
                         please create database and \
                         seed before continuing")

    
# Route for updating users details
# Takes ID of user and then user fields
# returns updated data to the user in JSON format
@users.route("/update/<int:id>", methods=["PUT"])
def update_user(id):
    pass
    user_fields = user_schema.load(request.json)

    user = db.get_or_404(User, id, description="User not found, please check id")

    user.first_name = user_fields["first_name"]
    user.last_name = user_fields["last_name"]
    user.email = user_fields["email"]
    user.password = bcrypt\
        .generate_password_hash(user_fields["password"])\
            .decode("utf-8")
    user.admin = False

    db.session.commit()


    return jsonify(user_schema.dump(user))
