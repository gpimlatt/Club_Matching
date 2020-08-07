import numpy
from flask import render_template, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from clubmatcher import app, db, bcrypt, mail
from clubmatcher.forms import (ClubForm, QuizForm, LoginForm,
                               RequestResetPasswordForm, ResetPasswordForm)
from clubmatcher.models import Club


@app.route("/")
def index():
    return render_template(
        'pages/index.html',
        title='USC Club Matcher'
    )


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('quiz'))
    form = ClubForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        club = Club(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password,
            facebook=form.facebook.data,
            instagram=form.instagram.data,
            twitter=form.twitter.data,
            website=form.website.data
        )
        if form.ecommerce.data:
            club.ecommerce = form.ecommerce.data
        db.session.add(club)
        db.session.commit()
        login_user(club)
        return redirect(url_for('quiz'))
    return render_template(
        'pages/register.html',
        title='Register Your Club',
        form=form
    )

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        club = Club.query.filter_by(email=form.email.data).first()
        if club and bcrypt.check_password_hash(club.password, form.password.data):
            login_user(club)
            return redirect(url_for('account'))
    return render_template(
        'pages/login.html',
        title='Login',
        form=form
    )


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/account")
@login_required
def account():
    return render_template(
        'pages/account.html',
        title='Club Information',
        club=current_user
    )

def euclidean_distance(user_answers, club_answers):
    results = []
    for name in club_answers:
        distance = numpy.linalg.norm(user_answers-club_answers[name])
        results.append((name, distance))
    return results

@app.route("/quiz", methods=['GET', 'POST'])
def quiz():
    form = QuizForm()
    if form.validate_on_submit():
        answers = form.q1.data + ',' \
                  + form.q2.data + ',' \
                  + form.q3.data + ',' \
                  + form.q4.data + ',' \
                  + form.q5.data
        if current_user.is_authenticated:
            current_user.answers = answers
            db.session.commit()
            return render_template(
                'pages/club_results.html',
                title='Quiz Completed'
            )
        else:
            user_answers = numpy.array((
                int(form.q1.data),
                int(form.q2.data),
                int(form.q3.data),
                int(form.q4.data),
                int(form.q5.data)
            ))
            all_club_answers= {}
            clubs = Club.query.all()
            for club in clubs:
                split_answers = club.answers.split(',')
                club_answers = ()
                for answer in split_answers:
                    club_answers += (int(answer),)
                all_club_answers[club.name] = numpy.array(club_answers)
            results = euclidean_distance(user_answers, all_club_answers)
            return render_template(
                'pages/user_results.html',
                title='Results',
                results=results
            )
    return render_template(
        'pages/quiz.html',
        title='Quiz',
        form=form
    )


# @app.route("/results", methods=['GET', 'POST'])
# def results():
#     if current_user.is_authenticated:
#         return render_template(
#             'pages/club_results.html',
#             title='Results'
#         )
#     else:
#         return render_template(
#             'pages/user_results.html',
#             title='Results'
#         )


def send_reset_email(club):
    token = club.get_reset_token()
    message = Message(
        'Password Reset Request',
        sender='noreply.westernusc.timeline@gmail.com',
        recipients=[club.email]
    )
    message.body = f'''
To reset your password, visit the following link:

{url_for('reset_password', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(message)


@app.route("/forgot", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        club = Club.query.filter_by(email=form.email.data).first()
        send_reset_email(club)
        return redirect(url_for('login'))
    return render_template(
        'pages/reset_request.html',
        title='Request Password Reset',
        form=form
    )


@app.route("/reset/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    club = Club.verify_reset_token(token)
    if not club:
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        club.password = hashed_password
        db.session.commit()
        login_user(club)
        return redirect(url_for('account'))
    return render_template(
        'pages/reset_password.html',
        title='Reset Password',
        form=form
    )
