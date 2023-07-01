"""Initializing Blogly application."""
from flask import Flask
from .models import db, connect_db
from .config import Config
from .routes import main, user
# from flask_debugtoolbar import DebugToolbarExtension


def create_app(config_name):
    """Creates the flask app context"""
    app = Flask(__name__)
    app.config.from_object(f"app.config.{config_name}")

    # toolbar = DebugToolbarExtension(app)

    connect_db(app)
    db.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(user)

    with app.app_context():
        from . import routes
        from . import models
        models.db.create_all()

    return app
