from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    # create the initial app instance
    app = Flask(__name__)

    # add the config file to the application
    app.config.from_object("config.app_config")

    # create the database within the app
    db.init_app(app)

    # create the serialization within the app
    ma.init_app(app)

    # Initialize bcrypt object within app
    bcrypt.init_app(app)

    # Initialize JWT object within app
    jwt.init_app(app)

    # register commands into the application
    from commands import db_commands
    app.register_blueprint(db_commands)
    
    # Import schemas into the application
    # This is to have all schemas registered into Marshmallow
    # upon first call
    from schemas import UserSchema


    # Register controller blueprints for all controllers
    from controllers import registerable_controllers

    for controller in registerable_controllers:
        app.register_blueprint(controller)

    return app