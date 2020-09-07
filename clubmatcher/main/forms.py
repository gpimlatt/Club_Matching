import flask
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, RadioField
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import DataRequired, Length
from clubmatcher.main.models import Club
from clubmatcher.main.questions import *


class UpdateClubForm(FlaskForm):
    ecommerce = URLField(
        'Western Store:',
        validators=[
            Length(max=2083)
        ]
    )
    facebook = URLField(
        'Facebook:',
        validators=[
            Length(max=2083)
        ]
    )
    instagram = URLField(
        'Instagram:',
        validators=[
            Length(max=2083)
        ]
    )
    twitter = URLField(
        'Twitter:',
        validators=[
            Length(max=2083)
        ]
    )
    website = URLField(
        'Club Website:',
        validators=[
            Length(max=2083)
        ]
    )
    submit = SubmitField(
        'Submit'
    )


class QuizForm(FlaskForm):
    q1_field = RadioField(
        flask.Markup(f"{q1}"),
        validators=[DataRequired()],
        choices=[
            ([1, 0, 0, 0], flask.Markup(f'<span>{q1_a1}</span>')),
            ([0, 1, 0, 0], flask.Markup(f'<span>{q1_a2}</span>')),
            ([0, 0, 1, 0], flask.Markup(f'<span>{q1_a3}</span>')),
            ([0, 0, 0, 1], flask.Markup(f'<span>{q1_a4}</span>'))
        ]
    )
    q2_field = RadioField(
        flask.Markup(f"{q2}"),
        validators=[DataRequired()],
        choices=[
            ([1,0,0,0,0,0,0,0,0], flask.Markup(f'<span>{q2_a1}</span>')),
            ([0,1,0,0,0,0,0,0,0], flask.Markup(f'<span>{q2_a2}</span>')),
            ([0,0,1,0,0,0,0,0,0], flask.Markup(f'<span>{q2_a3}</span>')),
            ([0,0,0,1,0,0,0,0,0], flask.Markup(f'<span>{q2_a4}</span>')),
            ([0,0,0,0,1,0,0,0,0], flask.Markup(f'<span>{q2_a5}</span>')),
            ([0,0,0,0,0,1,0,0,0], flask.Markup(f'<span>{q2_a6}</span>')),
            ([0,0,0,0,0,0,1,0,0], flask.Markup(f'<span>{q2_a7}</span>')),
            ([0,0,0,0,0,0,0,1,0], flask.Markup(f'<span>{q2_a8}</span>')),
            ([0,0,0,0,0,0,0,0,1], flask.Markup(f'<span>{q2_a9}</span>'))
        ]
    )
    q3_field = RadioField(
        flask.Markup(f"{q3}"),
        validators=[DataRequired()],
        choices=[
            (1, flask.Markup(f'<span>{q3_a1}</span>')),
            (2, flask.Markup(f'<span>{q3_a2}</span>')),
            (3, flask.Markup(f'<span>{q3_a3}</span>')),
            # (4, flask.Markup(f'<span>{q3_a4}</span>'))
        ]
    )
    q4_field = RadioField(
        flask.Markup(f"{q4}"),
        validators=[DataRequired()],
        choices=[
            (1, flask.Markup(f'<span>{q4_a1}</span>')),
            (2, flask.Markup(f'<span>{q4_a2}</span>')),
            (3, flask.Markup(f'<span>{q4_a3}</span>')),
            # (4, flask.Markup(f'<span>{q4_a4}</span>'))
        ]
    )
    q5_field = RadioField(
        flask.Markup(f"{q5}"),
        validators=[DataRequired()],
        choices=[
            (1, flask.Markup(f'<span>{q5_a1}</span>')),
            (2, flask.Markup(f'<span>{q5_a2}</span>')),
            (3, flask.Markup(f'<span>{q5_a3}</span>')),
            # (4, flask.Markup(f'<span>{q5_a4}</span>'))
        ]
    )
    submit = SubmitField(
        'Submit Quiz'
    )


class LoginForm(FlaskForm):
    email = EmailField(
        'Email:',
        validators=[
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password:',
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField(
        'Sign in'
    )
