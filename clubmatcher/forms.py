from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import DataRequired, Length, EqualTo

class ClubForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(max=120)
        ]
    )
    email = EmailField(
        'Email',
        validators=[
            DataRequired(),
            Length(max=120)
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8, max=30)
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )
    ecommerce = URLField(
        'eCommerce Page',
        validators=[
            Length(max=2083)
        ]
    )
    facebook = URLField(
        'Facebook',
        validators=[
            Length(max=2083)
        ]
    )
    instagram = URLField(
        'Instagram',
        validators=[
            Length(max=2083)
        ]
    )
    twitter = URLField(
        'Twitter',
        validators=[
            Length(max=2083)
        ]
    )
    website = URLField(
        'Club Website',
        validators=[
            Length(max=2083)
        ]
    )
    submit = SubmitField(
        'Submit'
    )
