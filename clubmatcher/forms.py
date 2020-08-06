from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import DataRequired, Length, EqualTo


class ClubForm(FlaskForm):
    name = StringField(
        'Club Name',
        validators=[
            DataRequired(),
            Length(max=120)
        ]
    )
    email = EmailField(
        'Club Admin Email',
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
        'Western Store',
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


class QuizForm(FlaskForm):
    q1 = RadioField(
        'Question 1',
        validators=[DataRequired()],
        choices=[
            (1, 'Answer 1'),
            (2, 'Answer 2'),
            (3, 'Answer 3'),
            (4, 'Answer 4')
        ]
    )
    q2 = RadioField(
        'Question 2',
        validators=[DataRequired()],
        choices=[
            (1, 'Answer 1'),
            (2, 'Answer 2'),
            (3, 'Answer 3'),
            (4, 'Answer 4')
        ]
    )
    q3 = RadioField(
        'Question 3',
        validators=[DataRequired()],
        choices=[
            (1, 'Answer 1'),
            (2, 'Answer 2'),
            (3, 'Answer 3'),
            (4, 'Answer 4')
        ]
    )
    submit = SubmitField(
        'Submit'
    )


class LoginForm(FlaskForm):
    email = EmailField(
        'Email',
        validators=[
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField(
        'Login'
    )
