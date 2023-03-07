from flask import Blueprint, jsonify, request, abort
from main import db
from models.user import User
from schemas.user_schema import user_schema, users_schema


users = Blueprint("user", __name__, url_prefix="/users")


# Get method for accessing all users, will implement Authorization in a bit
@users.route("/", methods=["GET"])
def get_users():

    users_list = User.query.all()

    result = users_schema.dump(users_list)

    return jsonify(result)
