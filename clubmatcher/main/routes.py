from numpy import dot
from numpy.linalg import norm
from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from clubmatcher import db, bcrypt, mail
from clubmatcher.main.forms import UpdateClubForm, QuizForm, LoginForm
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


@main.route("/account/update", methods=['GET', 'POST'])
@login_required
def update_account():
    form = UpdateClubForm()
    if form.validate_on_submit():
        current_user.ecommerce = form.ecommerce.data
        current_user.facebook = form.facebook.data
        current_user.instagram = form.instagram.data
        current_user.twitter = form.twitter.data
        current_user.website = form.website.data
        db.session.commit()
        flash('Your club information has been updated!', 'success')
        return redirect(url_for('main.account'))
    elif request.method == 'GET':
        form.ecommerce.data = current_user.ecommerce
        form.facebook.data = current_user.facebook
        form.instagram.data = current_user.instagram
        form.twitter.data = current_user.twitter
        form.website.data = current_user.website
    return render_template(
        'pages/update_account.html',
        title='Update Club Information',
        form=form
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
        answers = form.q1_field.data + ',' \
                  + form.q2_field.data + ',' \
                  + form.q3_field.data + ',' \
                  + form.q4_field.data + ',' \
                  + form.q5_field.data
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


def similarity(student, club):
    return dot(student, club) / (norm(student) * norm(club))

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
        form = QuizForm(request.form)
        q1_answers = form.q1_field.data[1:-1].split(',')
        q2_answers = form.q2_field.data[1:-1].split(',')
        q3_answers = form.q3_field.data
        q4_answers = form.q4_field.data
        q5_answers = form.q5_field.data
        print(q1_answers)

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
