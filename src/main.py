from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()

def create_app():

    app = Flask(__name__)

    app.config.from_object("config.app_config")

    db.init_app(app)

    ma.init_app(app)

    bcrypt.init_app(app)


    from commands import db_commands
    app.register_blueprint(db_commands)
    

    return app