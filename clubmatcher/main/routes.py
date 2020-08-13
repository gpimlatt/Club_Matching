import numpy
from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from clubmatcher import db, bcrypt, mail
from clubmatcher.main.forms import EditClubForm, QuizForm, LoginForm
from clubmatcher.main.models import Club

main = Blueprint('main', __name__)


@main.route("/")
def index():
    return render_template(
        'pages/index.html',
        title='USC Club Matcher'
    )


@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.quiz_completed:
            return redirect(url_for('main.account'))
        else:
            return redirect(url_for('main.quiz'))
    form = LoginForm()
    if form.validate_on_submit():
        club = Club.query.filter_by(email=form.email.data).first()
        if club and bcrypt.check_password_hash(club.password, form.password.data):
            login_user(club)
            flash('You have been logged in!', 'success')
            if club.quiz_completed:
                return redirect(url_for('main.account'))
            else:
                return redirect(url_for('main.quiz'))
    return render_template(
        'pages/login.html',
        title='Login',
        form=form
    )


@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route("/account")
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
        distance = numpy.linalg.norm(user_answers - club_answers[name])
        results.append((name, distance))
    return results


@main.route("/quiz", methods=['GET', 'POST'])
def quiz():
    if current_user.is_authenticated:
        form = QuizForm()
    else:
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
            flash('You have successfully completed the quiz!', 'success')
            return render_template(
                'pages/club_results.html',
                title='Confirmation'
            )
        else:
            # user_answers = numpy.array((
            #     int(form.q1.data),
            #     int(form.q2.data),
            #     int(form.q3.data),
            #     int(form.q4.data),
            #     int(form.q5.data)
            # ))
            # all_club_answers = {}
            # clubs = Club.query.all()
            # for club in clubs:
            #     split_answers = club.answers.split(',')
            #     club_answers = ()
            #     for answer in split_answers:
            #         club_answers += (int(answer),)
            #     all_club_answers[club.name] = numpy.array(club_answers)
            # results = euclidean_distance(user_answers, all_club_answers)
            results = Club.query.all()
            socials = {}
            for club in results:
                if club.facebook:
                    socials['facebook'] = club.facebook
                if club.instagram:
                    socials['instagram'] = club.instagram
                if club.twitter:
                    socials['twitter'] = club.twitter
                if club.website:
                    socials['website'] = club.website
            flash('You have successfully completed the quiz!', 'success')
            return render_template(
                'pages/user_results.html',
                title='Results',
                results=results,
                socials=socials
            )
    return render_template(
        'pages/quiz.html',
        title='Quiz',
        form=form
    )


@main.route("/results", methods=['GET', 'POST'])
def results():
    if request.method == 'GET':
        flash("You must complete the quiz first.")
        return redirect(url_for('main.quiz'))
    elif current_user.is_authenticated and QuizForm(request.form).validate_on_submit():
        return render_template(
            'pages/club_results.html',
            title='Results'
        )
    elif QuizForm(request.form).validate_on_submit():
        results = Club.query.all()
        socials = {}
        for club in results:
            if club.facebook:
                socials['facebook'] = club.facebook
            if club.instagram:
                socials['instagram'] = club.instagram
            if club.twitter:
                socials['twitter'] = club.twitter
            if club.website:
                socials['website'] = club.website
        return render_template(
            'pages/user_results.html',
            title='Results',
            results=results,
            socials=socials
        )
    else:
        form = QuizForm()
        flash('Please answer all quiz questions.')
        return render_template(
            'pages/quiz.html',
            title='Quiz',
            form=form
        )
