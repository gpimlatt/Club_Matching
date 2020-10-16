import os
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    with open('etc/config.json') as file:
        config = json.load(file)
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config.get('FLASK_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from clubmatcher.main.routes import main
    from clubmatcher.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
