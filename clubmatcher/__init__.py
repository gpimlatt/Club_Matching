import os
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()


def create_app():
    with open('etc/config.json') as file:
        config = json.load(file)
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config.get('FLASK_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = config.get('EMAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = config.get('EMAIL_PASSWORD')
    app.config['SERVER_NAME'] = 'localhost:5000'

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from clubmatcher.main.routes import main
    from clubmatcher.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
