from flask import Blueprint, render_template, redirect, request, flash, url_for
from .models import User, Post, Tag, PostTag, db
from sqlalchemy.exc import SQLAlchemyError
from .forms import NewUserForm, NewPostForm, NewTagForm

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
    form = NewUserForm()

    return render_template("users/new.html", form=form)


@user.route("/users/new", methods=["POST"])
def add_user():
    """Add user to users db with user input values"""
    form = NewUserForm()
    first_name = form.first_name.data
    last_name = form.last_name.data
    image_url = form.image_url.data

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('user.show_user_directory'))


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
    form = NewUserForm()
    user = User.query.filter_by(id=user_id).first()

    user.last_name = form.last_name.data
    user.first_name = form.first_name.data
    user.image_url = form.image_url.data
    db.session.commit()

    return redirect(url_for('user.show_user_directory'))


@user.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete user from users database"""
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect(url_for('user.show_user_directory'))


# ===================POSTS ROUTES===================
post = Blueprint('post', __name__)


@post.route("/users/<int:user_id>/posts/new")
def show_post_form(user_id):
    """Show a form to add a post for that user"""
    form = NewPostForm()

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template("posts/new.html", form=form, user=user, tags=tags)


@post.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_new_post(user_id):
    """Handle add form, add post and redirect to user's details page"""
    form = NewPostForm()
    user = User.query.get_or_404(user_id)

    if form.validate_on_submit():
        new_post = Post(title=form.title.data,
                        content=form.content.data, user_id=user.id)

        try:
            db.session.add(new_post)
            db.session.flush()

            tags = request.form.getlist("tag")

            for tag_name in tags:
                tag = Tag.query.filter_by(name=tag_name).first()
                if tag:
                    new_post_tag = PostTag(
                        post_id=new_post.id, tag_id=int(tag.id))
                    db.session.add(new_post_tag)

            db.session.commit()  # Commit changes after all tags are processed

        except SQLAlchemyError as e:
            print(str(e))
            db.session.rollback()

    return redirect(url_for('user.show_user', user_id=user_id))


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
    form = NewPostForm()
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    tags = Tag.query.all()

    return render_template("/posts/edit.html", user=user, post=post, tags=tags, form=form)


@post.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Handle editing of a post, redirect back to post detail view."""
    form = NewPostForm()
    post = Post.query.get_or_404(post_id)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data

        tag_names = request.form.getlist("tags")
        tags = Tag.query.filter(Tag.name.in_(tag_names)).all()
        post.tags = tags

        db.session.commit()

        return redirect(url_for('post.show_post', post_id=post_id))
    else:
        flash('Form submission failed. Please check your input.', 'error')
        return redirect(url_for('post.edit_post_form', post_id=post_id))


@post.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete a post from posts database"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)

    Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect(url_for('post.show_post', post_id=post_id))


# ==============TAG ROUTES====================
tag = Blueprint('tag', __name__)


@tag.route("/tags")
def show_all_tags():
    """Lists all tags with links to each tag's detail page"""
    tags = Tag.query.all()

    return render_template("/tags/alltags.html", tags=tags)


@tag.route("/tags/<int:tag_id>")
def show_tag_details(tag_id):
    """Show tag's detail page"""
    tag = Tag.query.get_or_404(tag_id)
    tagged_posts = tag.posts

    return render_template("/tags/details.html", tag=tag, tagged_posts=tagged_posts)


@tag.route("/tags/new")
def show_create_tag_form():
    """Show a form to create a tag"""
    form = NewTagForm()

    return render_template("/tags/new.html", form=form)


@tag.route("/tags/new", methods=["POST"])
def create_tag():
    """Create a tag, add to Tag table"""
    form = NewTagForm()
    if form.validate_on_submit():
        new_tag = Tag(name=form.name.data)

        db.session.add(new_tag)
        db.session.commit()

        return redirect(url_for('tag.show_all_tags'))
    else:
        flash('Form submission failed. Please check your input.', 'error')
        return render_template("/tags/new.html", form=form)


@tag.route("/tags/<int:tag_id>/edit")
def show_edit_tag_form(tag_id):
    """Show a form to edit a tag"""
    form = NewTagForm()
    tag = Tag.query.get_or_404(tag_id)

    return render_template("/tags/edit.html", tag=tag, form=form)


@tag.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Process edit form, update tag in db, redirect to tag list"""
    form = NewTagForm()
    tag = Tag.query.get_or_404(tag_id)

    if form.validate_on_submit():
        tag.name = form.name.data
        print(tag.name)

        db.session.commit()
        return redirect(url_for('tag.show_all_tags'))
    else:
        flash('Form submission failed. Please check your input.', 'error')
        return render_template("/tags/edit.html", form=form, tag=tag)


@tag.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Delete tag, update db"""
    tag = Tag.query.get_or_404(tag_id)
    print(tag)
    try:
        if tag:
            Tag.query.filter_by(id=tag_id).delete()
            db.session.commit()
        else:
            flash("Tag not found.", "error")
    except Exception as e:
        print(e)  # print exception for debugging
        db.session.rollback()
        flash('Delete failed.', 'error')
    return redirect(url_for('tag.show_all_tags'))
