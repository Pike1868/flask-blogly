from flask import Blueprint, render_template, redirect
from .models import User

# Create a Blueprint
main = Blueprint('main', __name__)


@main.route("/")
def index():
    """Show list of users"""
    return redirect("/users")


user = Blueprint('user', __name__)


@user.route("/users")
def show_user_directory():
    """Show a list of all users"""
    users = User.query.all()
    print(users)
    return render_template("index.html", users=users)
