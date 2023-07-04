from flask import Blueprint, render_template, redirect, request, flash
from .models import User, Post, db

# Create a Blueprint
main = Blueprint('main', __name__)


@main.route("/")
def index():
    """Show list of most recent posts"""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    
    return render_template("index.html", posts=posts)



user = Blueprint('user', __name__)


@user.route("/users")
def show_user_directory():
    """Show a list of all users"""
    users = User.query.all()

    return render_template("users.html", users=users)


@user.route("/users/new")
def create_user_form():
    """Show form to add a user"""
    return render_template("users/new.html")


@user.route("/users/<int:user_id>")
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user.id)
    return render_template("users/details.html", user=user, posts=posts)


@user.route("/users/new", methods=["POST"])
def add_user():
    """Add user to users db with user input values"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")


@user.route("/users/<int:user_id>/edit", methods=["GET"])
def edit_user_form(user_id):
    """Show form to edit a user"""
    user = User.query.get_or_404(user_id)
    return render_template("users/edit.html", user=user)


@user.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Show form to edit a user"""
    user = User.query.filter_by(id=user_id).first()

    user.last_name = request.form["last_name"]
    user.first_name = request.form["first_name"]
    user.image_url = request.form["image_url"]
    db.session.commit()

    return redirect("/users")


@user.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete user from users database"""
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect("/users")


post = Blueprint('post', __name__)


@post.route("/users/<int:user_id>/posts/new")
def show_post_form(user_id):
    """Show a form to add a post for that user"""
    user = User.query.get_or_404(user_id)
    return render_template("posts/new.html", user=user)


@post.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_new_post(user_id):
    """Handle add form, add post and redirect to user's details page"""
    user = User.query.get_or_404(user_id)

    new_post = Post(title=request.form["post_title"],
                    content=request.form["post_content"], user_id=user.id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user.id}")


@post.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show details about a single post"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)

    return render_template("/posts/details.html", user=user, post=post)


@post.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    """Show form to edit a post"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)

    return render_template("/posts/edit.html", user=user, post=post)


@post.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Handle editing of a post, redirect back to post detail view."""
    post = Post.query.get_or_404(post_id)

    post.title = request.form["post_title"]
    post.content = request.form["post_content"]

    db.session.commit()

    return redirect(f"/posts/{post_id}")


# to-do: add POST route for deleting a post: "/posts/[post_id]/delete"
@post.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete a post from posts database"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)

    Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect(f"/users/{user.id}")
