from wtforms import Form, StringField, DateField, validators, SubmitField
from flask_wtf import FlaskForm


class MovieForm(FlaskForm):
    release_date = DateField('Release Date', [validators.InputRequired()])
    title = StringField('Movie Title', [validators.Length(min=2, max=50)])
    submit = SubmitField(label='Add item')
