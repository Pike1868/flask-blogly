from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()
DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


def connect_db(app):
    """Connect to database."""
    db.app = app

# Models (schema) will go below


class User(db.Model):
    """Users table, will have id[PK], first_name, last_name, and image_url columns"""
    
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=False)
    image_url = db.Column(db.String(500), nullable=False,
                          default=DEFAULT_IMAGE_URL)

    @property
    def get_full_name(self):
        """Get full name of user"""

        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Posts table, will have id[PK], title, content, created_at, and user_id columns"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship("User", backref="user_posts")

    tags = db.relationship('Tag', secondary='post_tags')


    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


class Tag(db.Model):
    """Tag table, will have an id[PK] and a unique name"""
    
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    posts = db.relationship('Post', secondary='post_tags', backref='tags')
class PostTag(db.Model):
    """Table to join Post and Tag tables, will have [FK]s for both the post_id and the tag_id, composite [PK]"""
    
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    __table_args__ = (
        db.PrimaryKeyConstraint(
            post_id, tag_id,
        ),)
