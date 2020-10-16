from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from clubmatcher import db, bcrypt
from clubmatcher.main.forms import UpdateClubForm, QuizForm, LoginForm
from clubmatcher.main.models import Club, Statistic
from clubmatcher.main.utils import cosine_similarity, update_quiz_counter

main = Blueprint('main', __name__)


@main.route("/")
def index():
    """Route for the website's index page.

    Returns:
        A rendered html template for this route.
    """
    return render_template(
        'pages/index.html',
        title='USC Club Matcher'
    )


@main.route("/login", methods=['GET', 'POST'])
def login():
    """Route for club login page.

    Returns:
        If the club is logged-in and then have not yet completed
        the quiz, then a redirect to the quiz route in the main module will be
        returned.
        If the club is logged-in and they have previously completed
        the quiz, then a redirect to the account route in the main module will
        be returned.
        Otherwise, a rendered html template for this route will be returned.
    """
    if current_user.is_authenticated:
        if current_user.answers:
            return redirect(url_for('main.account'))
        else:
            return redirect(url_for('main.quiz'))
    form = LoginForm()
    if form.validate_on_submit():
        club = Club.query.filter_by(email=form.email.data).first()
        if club and bcrypt.check_password_hash(club.password, form.password.data):
            login_user(club)
            if club.answers:
                return redirect(url_for('main.account'))
            else:
                return redirect(url_for('main.quiz'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'error')
    return render_template(
        'pages/login.html',
        title='Login',
        form=form
    )


@main.route("/logout")
def logout():
    """Route for logging a club out of their account.

    Returns:
        A redirect for the index route in the main module.
    """
    logout_user()
    return redirect(url_for('main.index'))


@main.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """Route for the club's account page.

    Returns:
        A rendered html page for this route.
    """
    form = UpdateClubForm()
    quiz_completed = True if current_user.answers else False
    if form.validate_on_submit():
        current_user.facebook = form.facebook.data
        current_user.instagram = form.instagram.data
        current_user.twitter = form.twitter.data
        current_user.website = form.website.data
        db.session.commit()
        flash('Your club information has been updated!', 'success')
    elif request.method == 'GET':
        form.facebook.data = current_user.facebook
        form.instagram.data = current_user.instagram
        form.twitter.data = current_user.twitter
        form.website.data = current_user.website
    return render_template(
        'pages/update_account.html',
        title='Update Club Information',
        form=form,
        quiz_completed=quiz_completed
    )


@main.route("/quiz", methods=['GET', 'POST'])
def quiz():
    """Route for the quiz page.

    Returns:
        A rendered html template for this route.
    """
    form = QuizForm()
    return render_template(
        'pages/quiz.html',
        title='Quiz',
        form=form
    )


@main.route("/results", methods=['GET', 'POST'])
def results():
    """Route for displaying the quiz results

    Returns:
        If the quiz has not yet been completed, a redirect to the quiz route
        in the main module will be returned.
        If the all the quiz question have not been answered, then a rendered
        html template for the quiz route will be returned.
        If a club admin submits the quiz, then a redirect to the club's account
        page will be returned.
        If a user submits the quiz, then a rendered html template for this route
        will be returned.
    """
    if request.method == 'GET':
        flash("You must complete the quiz first.", "error")
        return redirect(url_for('main.quiz'))
    elif QuizForm(request.form).validate_on_submit():
        form = QuizForm(request.form)
        q1 = form.q1_field.data[1:-1].split(',')
        q2 = form.q2_field.data[1:-1].split(',')
        q3 = form.q3_field.data
        q4 = form.q4_field.data
        q5 = form.q5_field.data
        q6 = form.q6_field.data
        q7 = form.q7_field.data
        q8 = form.q8_field.data[1:-1].split(',')
        if current_user.is_authenticated:
            club_answers = ''.join(q1).replace(' ', ',') + ',' + \
                           ''.join(q2).replace(' ', ',') + ',' + \
                           q3 + ',' + q4 + ',' + q5 + ',' + q6 + ',' + q7 + ',' + \
                           ''.join(q8).replace(' ', ',')
            current_user.answers = club_answers
            db.session.commit()
            flash('Thank you, your answers have been recorded!', 'success')
            return redirect(url_for('main.account'))
        else:
            update_quiz_counter()
            student_answers = q1 + q2
            student_answers.extend([q3, q4, q5, q6, q7])
            student_answers = student_answers + q8
            student_answers = [int(answer) for answer in student_answers]
            recommended_club_ids = {}
            clubs = Club.query.all()
            for club in clubs:
                if club.answers:
                    club_answers = club.answers.split(',')
                    club_answers = [int(answer) for answer in club_answers]
                    similarity_score = cosine_similarity(
                        student_answers,
                        club_answers
                    )
                    if len(recommended_club_ids) < 5:
                        recommended_club_ids[club.id] = similarity_score
                        recommended_club_ids = {k: v for k, v in sorted(
                            recommended_club_ids.items(),
                            key=lambda item: item[1]
                        )}
                    else:
                        for club_id in list(recommended_club_ids):
                            if recommended_club_ids[club_id] < similarity_score:
                                del recommended_club_ids[club_id]
                                recommended_club_ids[club.id] = similarity_score
                                recommended_club_ids = {k: v for k, v in sorted(
                                    recommended_club_ids.items(),
                                    key=lambda item: item[1]
                                )}
                                break
            recommended_clubs = []
            recommended_club_ids = {k: v for k, v in sorted(
                recommended_club_ids.items(),
                key=lambda item: item[1],
                reverse=True
            )}
            for id in recommended_club_ids:
                recommended_clubs.append(Club.query.get(id))
            return render_template(
                'pages/user_results.html',
                title='Results',
                recommended_clubs=recommended_clubs,
            )
    else:
        form = QuizForm()
        flash('Please answer all quiz questions.', 'error')
        return render_template(
            'pages/quiz.html',
            title='Quiz',
            form=form
        )
