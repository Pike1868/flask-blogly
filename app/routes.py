from flask import Blueprint, render_template, redirect, request, flash
from .models import User, Post, Tag, PostTag, db
from sqlalchemy.exc import SQLAlchemyError

main = Blueprint('main', __name__)


@main.route("/")
def index():
    """Show list of most recent posts"""
    posts = Post.query.order_by(Post.created_at.desc()).all()

    return render_template("index.html", posts=posts)


# ===============USER ROUTES==================
user = Blueprint('user', __name__)


@user.route("/users")
def show_user_directory():
    """Show a list of all users"""
    users = User.query.all()

    return render_template("users.html", users=users)


@user.route("/users/new")
def show_create_user_form():
    """Show form to add a user"""
    return render_template("users/new.html")


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


@user.route("/users/<int:user_id>")
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user.id)
    return render_template("users/details.html", user=user, posts=posts)


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


# ===================POSTS ROUTES===================
post = Blueprint('post', __name__)


@post.route("/users/<int:user_id>/posts/new")
def show_post_form(user_id):
    """Show a form to add a post for that user"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("posts/new.html", user=user, tags=tags)


@post.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_new_post(user_id):
    """Handle add form, add post and redirect to user's details page"""
    user = User.query.get_or_404(user_id)
    print(f"THIS SHOULD BE THE USER ID: {user.id}")
    new_post = Post(title=request.form["post_title"],
                    content=request.form["post_content"], user_id=user.id)

    try:
        db.session.add(new_post)
        db.session.flush()  # make sure new_post has an ID before committing

        tags = request.form.getlist("tag")
        print(tags)

        for tag in tags:
            tag = Tag.query.filter_by(name=tag).first()
            new_post_tag = PostTag(post_id=new_post.id, tag_id=int(tag.id))
            db.session.add(new_post_tag)

        db.session.commit()
    except SQLAlchemyError as e:
        print(str(e))
        db.session.rollback()

    return redirect(f"/users/{user.id}")


@post.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show details about a single post"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    tags = post.tags

    return render_template("/posts/details.html", user=user, post=post, tags=tags)


@post.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    """Show form to edit a post"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    tags = Tag.query.all()

    return render_template("/posts/edit.html", user=user, post=post, tags=tags)


@post.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Handle editing of a post, redirect back to post detail view."""
    post = Post.query.get_or_404(post_id)

    post.title = request.form["post_title"]
    post.content = request.form["post_content"]

    tag_names = request.form.getlist("tags")
    print(tag_names)

    tags = Tag.query.filter(Tag.name.in_(tag_names)).all()
    post.tags = tags

    print("++++++++++++++++++++++++++++++++")
    print(tags)
    print(post.tags)
    print("++++++++++++++++++++++++++++++++")

    db.session.commit()

    return redirect(f"/posts/{post_id}")


@post.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete a post from posts database"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)

    Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect(f"/users/{user.id}")


# ==============TAG ROUTES====================
tag = Blueprint('tag', __name__)


@tag.route("/tags")
def show_all_tags():
    """Lists all tags with links to each tag's detail page"""
    tags = Tag.query.all()
    print(tags)

    return render_template("/tags/alltags.html", tags=tags)


@tag.route("/tags/<int:tag_id>")
def show_tag_details(tag_id):
    """Show tag's detail page"""
    tag = Tag.query.get_or_404(tag_id)
    tagged_posts = tag.posts
    print(f"Tag: {tag}")
    print(f"Tagged posts: {tagged_posts}")
    return render_template("/tags/details.html", tag=tag, tagged_posts=tagged_posts)


@tag.route("/tags/new")
def show_create_tag_form():
    """Show a form to create a tag"""
    return render_template("/tags/new.html")


@tag.route("/tags/new", methods=["POST"])
def create_tag():
    """Create a tag, add to Tag table"""
    new_tag = Tag(name=request.form["tag_name"])
    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")


@tag.route("/tags/<int:tag_id>/edit")
def show_edit_tag_form(tag_id):
    """Show a form to edit a tag"""

    tag = Tag.query.get_or_404(tag_id)

    return render_template("/tags/edit.html", tag=tag)


@tag.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Process edit form, update tag in db, redirect to tag list"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["tag_name"]

    db.session.commit()
    return redirect("/tags")

# 7. To-do: POST route /tags/[tag-id]/delete = Delete a tag


@tag.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Delete tag, update db"""
    Tag.query.filter_by(id=tag_id).delete()

    db.session.commit()
    return redirect("/tags")
