from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from . import models

class BlogForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(message="Title cannot be empty")])
    category = StringField('category', validators=[DataRequired(message="Category cannot be empty")])
    content = TextAreaField('content', validators=[DataRequired(message="Content cannot be empty")])
    submit = SubmitField('Submit')

class EditPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Update Post')

