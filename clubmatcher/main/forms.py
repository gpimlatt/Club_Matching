import flask
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, RadioField
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import DataRequired, Length
from clubmatcher.main.models import Club
from clubmatcher.main.questions import *


class UpdateClubForm(FlaskForm):
    ecommerce = URLField(
        'Western USC Store Page',
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
        'Update'
    )


class QuizForm(FlaskForm):
    q1_field = RadioField(
        flask.Markup(f"{q1}"),
        validators=[DataRequired()],
        choices=[
            ([1, 0, 0, 0, 0], flask.Markup(f'<span>{q1_answers[1]}</span>')),
            ([0, 1, 0, 0, 0], flask.Markup(f'<span>{q1_answers[2]}</span>')),
            ([0, 0, 1, 0, 0], flask.Markup(f'<span>{q1_answers[3]}</span>')),
            ([0, 0, 0, 1, 0], flask.Markup(f'<span>{q1_answers[4]}</span>')),
            ([0, 0, 0, 0, 1], flask.Markup(f'<span>{q1_answers[5]}</span>'))
        ]
    )
    q2_field = RadioField(
        flask.Markup(f"{q2}"),
        validators=[DataRequired()],
        choices=[
            ([1, 0, 0, 0, 0, 0, 0, 0, 0], flask.Markup(f'<span>{q2_answers[1]}</span>')),
            ([0, 1, 0, 0, 0, 0, 0, 0, 0], flask.Markup(f'<span>{q2_answers[2]}</span>')),
            ([0, 0, 1, 0, 0, 0, 0, 0, 0], flask.Markup(f'<span>{q2_answers[3]}</span>')),
            ([0, 0, 0, 1, 0, 0, 0, 0, 0], flask.Markup(f'<span>{q2_answers[4]}</span>')),
            ([0, 0, 0, 0, 1, 0, 0, 0, 0], flask.Markup(f'<span>{q2_answers[5]}</span>')),
            ([0, 0, 0, 0, 0, 1, 0, 0, 0], flask.Markup(f'<span>{q2_answers[6]}</span>')),
            ([0, 0, 0, 0, 0, 0, 1, 0, 0], flask.Markup(f'<span>{q2_answers[7]}</span>')),
            ([0, 0, 0, 0, 0, 0, 0, 1, 0], flask.Markup(f'<span>{q2_answers[8]}</span>')),
            ([0, 0, 0, 0, 0, 0, 0, 0, 1], flask.Markup(f'<span>{q2_answers[9]}</span>'))
        ]
    )
    q3_field = RadioField(
        flask.Markup(f"{q3}"),
        validators=[DataRequired()],
        choices=[
            (1, flask.Markup(f'<span>{q3_answers[1]}</span>')),
            (2, flask.Markup(f'<span>{q3_answers[2]}</span>')),
            (3, flask.Markup(f'<span>{q3_answers[3]}</span>'))
        ]
    )
    q4_field = RadioField(
        flask.Markup(f"{q4}"),
        validators=[DataRequired()],
        choices=[
            (1, flask.Markup(f'<span>{q4_answers[1]}</span>')),
            (2, flask.Markup(f'<span>{q4_answers[2]}</span>')),
            (3, flask.Markup(f'<span>{q4_answers[3]}</span>'))
        ]
    )
    q5_field = RadioField(
        flask.Markup(f"{q5}"),
        validators=[DataRequired()],
        choices=[
            (1, flask.Markup(f'<span>{q5_answers[1]}</span>')),
            (2, flask.Markup(f'<span>{q5_answers[2]}</span>')),
            (3, flask.Markup(f'<span>{q5_answers[3]}</span>'))
        ]
    )
    q6_field = RadioField(
        flask.Markup(f"{q6}"),
        validators=[DataRequired()],
        choices=[
            (1, flask.Markup(f'<span>{q6_answers[1]}</span>')),
            (2, flask.Markup(f'<span>{q6_answers[2]}</span>')),
            (3, flask.Markup(f'<span>{q6_answers[3]}</span>'))
        ]
    )
    q7_field = RadioField(
        flask.Markup(f"{q7}"),
        validators=[DataRequired()],
        choices=[
            (1, flask.Markup(f'<span>{q7_answers[1]}</span>')),
            (2, flask.Markup(f'<span>{q7_answers[2]}</span>')),
            (3, flask.Markup(f'<span>{q7_answers[3]}</span>'))
        ]
    )
    q8_field = RadioField(
        flask.Markup(f"{q8}"),
        validators=[DataRequired()],
        choices=[
            ([1, 0], flask.Markup(f'<span>{q8_answers[1]}</span>')),
            ([0, 1], flask.Markup(f'<span>{q8_answers[2]}</span>'))
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
