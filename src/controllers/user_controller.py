from flask import Blueprint, jsonify, request, abort
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

    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, "Incorrect password or email")
    
    return "Password accepted"

    