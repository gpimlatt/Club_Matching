from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from clubmatcher.main.models import Club


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

    def validate_name(self, name):
        club = Club.query.filter_by(name=name.data).first()
        if club:
            raise ValidationError('That name is taken. Please choose another.')

    def validate_email(self, email):
        club = Club.query.filter_by(email=email.data).first()
        if club:
            raise ValidationError('That email is taken. Please choose another.')


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
    q4 = RadioField(
        'Question 4',
        validators=[DataRequired()],
        choices=[
            (1, 'Answer 1'),
            (2, 'Answer 2'),
            (3, 'Answer 3'),
            (4, 'Answer 4')
        ]
    )
    q5 = RadioField(
        'Question 5',
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


class RequestResetPasswordForm(FlaskForm):
    email = EmailField(
        'Email',
        validators=[DataRequired()])
    submit = SubmitField(
        'Submit'
    )

    def validate_email(self, email):
        club = Club.query.filter_by(email=email.data).first()
        if not club:
            raise ValidationError('There is no account with that email.')


class ResetPasswordForm(FlaskForm):
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
    submit = SubmitField(
        'Reset'
    )
