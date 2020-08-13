import flask
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, RadioField
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import DataRequired, Length
from clubmatcher.main.models import Club


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
    q1_text = 'What is your favorite thing to do on campus?'
    q2_text = 'What is your favorite color?'
    q3_text = 'What is your favorite thing about Western?'
    q4_text = 'Which faculty are you apart of?'
    q5_text = 'What year are you currently in?'

    q1 = RadioField(
        flask.Markup(f'<b>Question 1:</b> {q1_text}'),
        validators=[DataRequired()],
        choices=[
            (1, flask.Markup('<span>Answer 1</span>')),
            (2, flask.Markup('<span>Answer 2</span>')),
            (3, flask.Markup('<span>Answer 3</span>')),
            (4, flask.Markup('<span>Answer 4</span>'))
        ]
    )
    q2 = RadioField(
        flask.Markup(f"<b>Question 2:</b> {q2_text}"),
        validators=[DataRequired()],
        choices=[
            (1, flask.Markup('<span>Answer 1</span>')),
            (2, flask.Markup('<span>Answer 2</span>')),
            (3, flask.Markup('<span>Answer 3</span>')),
            (4, flask.Markup('<span>Answer 4</span>'))
        ]
    )
    q3 = RadioField(
        flask.Markup(f"<b>Question 3:</b> {q3_text}"),
        validators=[DataRequired()],
        choices=[
            (1, flask.Markup('<span>Answer 1</span>')),
            (2, flask.Markup('<span>Answer 2</span>')),
            (3, flask.Markup('<span>Answer 3</span>')),
            (4, flask.Markup('<span>Answer 4</span>'))
        ]
    )
    q4 = RadioField(
        flask.Markup(f"<b>Question 4:</b> {q4_text}"),
        validators=[DataRequired()],
        choices=[
            (1, flask.Markup('<span>Answer 1</span>')),
            (2, flask.Markup('<span>Answer 2</span>')),
            (3, flask.Markup('<span>Answer 3</span>')),
            (4, flask.Markup('<span>Answer 4</span>'))
        ]
    )
    q5 = RadioField(
        flask.Markup(f"<b>Question 5:</b> {q5_text}"),
        validators=[DataRequired()],
        choices=[
            (1, flask.Markup('<span>Answer 1</span>')),
            (2, flask.Markup('<span>Answer 2</span>')),
            (3, flask.Markup('<span>Answer 3</span>')),
            (4, flask.Markup('<span>Answer 4</span>'))
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
        'Login'
    )
