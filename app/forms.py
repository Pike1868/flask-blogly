from flask_wtf import FlaskForm
from wtforms import StringField, FloatField


class NewUserForm(FlaskForm):
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    image_url = StringField("Profile Image")


class NewPostForm(FlaskForm):
    title = StringField("Title")
    content = StringField("Content")


class NewTagForm(FlaskForm):
    name = StringField("Tag Name")
