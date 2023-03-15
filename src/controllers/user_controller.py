from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import timedelta
from decorators.error_decorator import error_handlers
from decorators.user_login import get_admin_user, get_user_fromdb
from main import db, bcrypt
from models.user import User
from models.attending import Attending
from schemas.user_schema import user_schema, UserSchema
from schemas.attending_schema import attending_schema, attending_schemas


users = Blueprint("user", __name__, url_prefix="/users")


# Get method for accessing all users
# Initial user has to be admin to be allowed to view the list of users
# method takes the id of the admin which is 1
# method returns serialized information of users.
# only id, first and last names, and email
@users.route("/<int:id>", methods=["GET"])
# @jwt_required()
@get_admin_user
def get_users(id):

    # user = get_jwt_identity()
    users_list = User.query.all()

    result = UserSchema(only=["id", "first_name", "last_name", "email"], many=True)

    return jsonify(result.dump(users_list))


# Get method for displaying single user, including bands and venues they own
# Function takes user Id to and authenticates through JWT to ensure 
# user is authorized/authenticated.
# returns user information within json object
@users.route("/display_user/<int:user_id>", methods=["GET"])
@get_user_fromdb
def display_user(user):

    return jsonify(user_schema.dump(user))


# Get method for displaying contents of attending table
@users.route("/attending/show", methods=["GET"])
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
    
    expiry = timedelta(days=1)
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
    
    return jsonify({"user" : user.email, "token" : access_token})


# Post method to register new user into database,
# Takes user fields through input via JSON on postman/insomnia
# Returns user token and registration message
@users.route("/register", methods=["POST"])
@error_handlers
def user_register():
    
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
    
    
    expiry = timedelta(days=1)
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
    
    return jsonify({"user" : user.email, "token" : access_token})


# Route for updating users details
# Takes ID of user and then user fields
# returns updated data to the user in JSON format
@users.route("/update/<int:user_id>", methods=["PUT"])
# @error_handlers
@get_user_fromdb
def update_user(user):

    user_fields = user_schema.load(request.json)
    
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
# method requires user to submit their id, checking that id is authorized 
# then deleting user and returning message informing user is deleted
@users.route("/delete/<int:user_id>/<int:id>", methods=["DELETE"])
@get_user_fromdb
# @error_handlers
def delete_user(user, id,):


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
# method takes user id to authenticate user
# method takes the show_id as a field to validate through schema
# returns json object of the upcoming show attendance
@users.route("/attending/register/<int:id>", methods=["POST"])
@jwt_required()
@error_handlers
def register_attendance(id):
    user = get_jwt_identity()

    user = db.get_or_404(User, id, description="User not found")

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
@users.route("/attending/remove/<int:id>/<int:attending_id>", methods=["DELETE"])
@jwt_required()
@error_handlers
def remove_attendance(id, attending_id):
    user = get_jwt_identity()

    user = db.get_or_404(User, id, description="User not found")

    attending = db.get_or_404(Attending, attending_id, description="record not found")

    if user.id != attending.user_id:
        return {"message" : "Sorry you do not have access to this attendance"}, 401
    
    db.session.delete(attending)
    db.session.commit()

    return {"message" : "attendance removed"}, 200